'use client';

import React from 'react';
import type { LeadInsight } from '@/types';
import { TrendingUp } from 'lucide-react';

interface LeadInsightPanelProps {
  insights: LeadInsight | null;
}

export const LeadInsightPanel: React.FC<LeadInsightPanelProps> = ({ insights }) => {
  if (!insights) {
    return (
      <div className="card text-center text-gray-500">
        <p>No insights yet. Start a conversation to extract lead data.</p>
      </div>
    );
  }

  return (
    <div className="card space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp size={20} className="text-blue-600" />
        <h3 className="font-bold text-gray-900">Lead Insights</h3>
      </div>

      {insights.budget_min && insights.budget_max && (
        <div>
          <p className="text-sm text-gray-600">Budget Range</p>
          <p className="font-semibold text-gray-900">
            ${insights.budget_min.toLocaleString()} - $
            {insights.budget_max.toLocaleString()}
          </p>
        </div>
      )}

      {insights.preferred_locations.length > 0 && (
        <div>
          <p className="text-sm text-gray-600">Preferred Locations</p>
          <div className="flex flex-wrap gap-2">
            {insights.preferred_locations.map((loc, idx) => (
              <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                {loc}
              </span>
            ))}
          </div>
        </div>
      )}

      {insights.property_types.length > 0 && (
        <div>
          <p className="text-sm text-gray-600">Property Types</p>
          <div className="flex flex-wrap gap-2">
            {insights.property_types.map((type, idx) => (
              <span key={idx} className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm capitalize">
                {type}
              </span>
            ))}
          </div>
        </div>
      )}

      {insights.urgency && (
        <div>
          <p className="text-sm text-gray-600">Urgency</p>
          <span className={`inline-block px-2 py-1 rounded text-sm font-semibold capitalize ${
            insights.urgency === 'high' ? 'bg-red-100 text-red-800' :
            insights.urgency === 'medium' ? 'bg-yellow-100 text-yellow-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {insights.urgency}
          </span>
        </div>
      )}

      <div>
        <p className="text-sm text-gray-600">Buying Intent Score</p>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full"
            style={{ width: `${insights.buying_intent_score * 100}%` }}
          ></div>
        </div>
        <p className="text-sm font-semibold text-gray-900 mt-1">
          {(insights.buying_intent_score * 100).toFixed(0)}%
        </p>
      </div>

      {insights.objections.length > 0 && (
        <div>
          <p className="text-sm text-gray-600">Objections</p>
          <ul className="list-disc list-inside space-y-1">
            {insights.objections.map((obj, idx) => (
              <li key={idx} className="text-sm text-gray-700">
                {obj}
              </li>
            ))}
          </ul>
        </div>
      )}

      {insights.preferred_amenities.length > 0 && (
        <div>
          <p className="text-sm text-gray-600">Preferred Amenities</p>
          <div className="flex flex-wrap gap-2">
            {insights.preferred_amenities.map((amenity, idx) => (
              <span key={idx} className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm">
                {amenity}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
