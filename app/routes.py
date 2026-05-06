import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from geopy.distance import geodesic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Address
from app.schemas import AddressCreate, AddressOut, AddressUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressOut, status_code=201)
async def create_address(payload: AddressCreate, db: AsyncSession = Depends(get_db)):
    """Create a new address entry."""
    address = Address(**payload.model_dump())
    db.add(address)
    await db.commit()
    await db.refresh(address)
    logger.info(f"Created address id={address.id}")
    return address


@router.get("/", response_model=List[AddressOut])
async def list_addresses(db: AsyncSession = Depends(get_db)):
    """Get all addresses."""
    result = await db.execute(select(Address))
    addresses = result.scalars().all()
    return addresses


@router.get("/nearby", response_model=List[AddressOut])
async def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90, description="Your latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Your longitude"),
    distance_km: float = Query(10.0, gt=0, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns all addresses within a given distance (km) from the provided coordinates.
    Uses geodesic distance (accounts for Earth's curvature).
    """
    result = await db.execute(select(Address))
    all_addresses = result.scalars().all()

    origin = (latitude, longitude)
    nearby = []

    for addr in all_addresses:
        point = (addr.latitude, addr.longitude)
        dist = geodesic(origin, point).kilometers
        if dist <= distance_km:
            nearby.append(addr)

    logger.info(
        f"Nearby search from ({latitude},{longitude}) within {distance_km}km → {len(nearby)} results"
    )
    return nearby


@router.get("/{address_id}", response_model=AddressOut)
async def get_address(address_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single address by ID."""
    address = await db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=AddressOut)
async def update_address(
    address_id: int, payload: AddressUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an existing address. Only provided fields will be updated."""
    address = await db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    updated_fields = payload.model_dump(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)
    logger.info(f"Updated address id={address_id}, fields={list(updated_fields.keys())}")
    return address


@router.delete("/{address_id}", status_code=204)
async def delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an address by ID."""
    address = await db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    await db.delete(address)
    await db.commit()
    logger.info(f"Deleted address id={address_id}")
