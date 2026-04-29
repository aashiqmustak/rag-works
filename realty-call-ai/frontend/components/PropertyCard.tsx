'use client';

import React from 'react';
import type { Property } from '@/types';

interface PropertyCardProps {
  property: Property;
  onClick?: (property: Property) => void;
}

export const PropertyCard: React.FC<PropertyCardProps> = ({
  property,
  onClick,
}) => {
  return (
    <div className="card cursor-pointer" onClick={() => onClick?.(property)}>
      <div className="mb-3">
        <h3 className="text-lg font-bold text-gray-900">{property.title}</h3>
        <p className="text-sm text-gray-600">{property.location}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
        <div>
          <span className="text-gray-600">Price:</span>
          <p className="font-semibold text-blue-600">
            ${property.price.toLocaleString()}
          </p>
        </div>
        <div>
          <span className="text-gray-600">Type:</span>
          <p className="font-semibold capitalize">{property.property_type}</p>
        </div>
        <div>
          <span className="text-gray-600">Beds:</span>
          <p className="font-semibold">{property.bedrooms}</p>
        </div>
        <div>
          <span className="text-gray-600">Baths:</span>
          <p className="font-semibold">{property.bathrooms}</p>
        </div>
      </div>

      <div className="mb-3">
        <p className="text-sm text-gray-600 line-clamp-2">
          {property.description}
        </p>
      </div>

      {property.amenities.length > 0 && (
        <div className="mb-3">
          <div className="flex flex-wrap gap-1">
            {property.amenities.slice(0, 3).map((amenity, idx) => (
              <span
                key={idx}
                className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded"
              >
                {amenity}
              </span>
            ))}
            {property.amenities.length > 3 && (
              <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">
                +{property.amenities.length - 3}
              </span>
            )}
          </div>
        </div>
      )}

      <div className="text-right">
        <button className="btn-primary text-sm">View Details</button>
      </div>
    </div>
  );
};

interface PropertyGridProps {
  properties: Property[];
  onPropertyClick?: (property: Property) => void;
}

export const PropertyGrid: React.FC<PropertyGridProps> = ({
  properties,
  onPropertyClick,
}) => {
  if (properties.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No properties found</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {properties.map((property) => (
        <PropertyCard
          key={property.id}
          property={property}
          onClick={onPropertyClick}
        />
      ))}
    </div>
  );
};
