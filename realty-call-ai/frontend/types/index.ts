export type PropertyType = 'apartment' | 'villa' | 'house' | 'commercial' | 'land';

export interface Property {
  id: string;
  title: string;
  description: string;
  price: number;
  property_type: PropertyType;
  location: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  amenities: string[];
  images: string[];
  availability: boolean;
  agent_name?: string;
  agent_phone?: string;
}

export interface ChatMessage {
  id: string;
  lead_id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  source: string;
  sales_stage: string;
  insights?: LeadInsight;
  properties_viewed: string[];
  created_at: string;
  updated_at: string;
}

export interface LeadInsight {
  budget_min?: number;
  budget_max?: number;
  preferred_locations: string[];
  property_types: PropertyType[];
  urgency?: 'high' | 'medium' | 'low';
  objections: string[];
  buying_intent_score: number;
  preferred_amenities: string[];
  family_size?: number;
  move_timeline?: string;
}

export interface ChatResponse {
  response: string;
  properties_recommended: Property[];
  lead_insights?: LeadInsight;
  action_items: string[];
}

export interface Call {
  call_id: string;
  phone_number: string;
  lead_name: string;
  status: 'initiated' | 'ringing' | 'connected' | 'completed' | 'failed';
  created_at: string;
  ended_at?: string;
  summary?: Record<string, any>;
}
