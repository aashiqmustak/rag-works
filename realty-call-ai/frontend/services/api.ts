import axios, { AxiosInstance } from 'axios';
import type { ChatResponse, ChatMessage, Property, Lead, Call } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Chat endpoints
  async sendMessage(leadId: string, message: string): Promise<ChatResponse> {
    const response = await this.client.post('/api/chat/send', {
      lead_id: leadId,
      message,
    });
    return response.data;
  }

  async getChatHistory(leadId: string): Promise<{ history: ChatMessage[] }> {
    const response = await this.client.get(`/api/chat/history/${leadId}`);
    return response.data;
  }

  async clearChatHistory(leadId: string): Promise<void> {
    await this.client.delete(`/api/chat/history/${leadId}`);
  }

  // Property endpoints
  async searchProperties(query: string, topK: number = 5): Promise<Property[]> {
    const response = await this.client.post('/api/properties/search', {
      query,
      top_k: topK,
    });
    return response.data.results;
  }

  async filterProperties(filters: Record<string, any>): Promise<Property[]> {
    const response = await this.client.post('/api/properties/filter', filters);
    return response.data;
  }

  async getPropertyCount(): Promise<{ total_properties: number }> {
    const response = await this.client.get('/api/properties/count');
    return response.data;
  }

  // Lead endpoints
  async createLead(name: string, email: string, phone: string): Promise<{ lead_id: string }> {
    const response = await this.client.post('/api/leads/create', null, {
      params: { name, email, phone },
    });
    return response.data;
  }

  async getLead(leadId: string): Promise<Lead> {
    const response = await this.client.get(`/api/leads/${leadId}`);
    return response.data;
  }

  async updateLead(leadId: string, data: Partial<Lead>): Promise<void> {
    await this.client.put(`/api/leads/${leadId}`, data);
  }

  async updateLeadInsights(leadId: string, insights: any): Promise<void> {
    await this.client.put(`/api/leads/${leadId}/insights`, insights);
  }

  async listLeads(): Promise<{ total: number; leads: Lead[] }> {
    const response = await this.client.get('/api/leads');
    return response.data;
  }

  // Call endpoints
  async initiateCall(phoneNumber: string, leadName: string): Promise<{ call_id: string }> {
    const response = await this.client.post('/api/calls/initiate', {
      phone_number: phoneNumber,
      lead_name: leadName,
    });
    return response.data;
  }

  async getCallStatus(callId: string): Promise<Call> {
    const response = await this.client.get(`/api/calls/${callId}`);
    return response.data;
  }

  async endCall(callId: string, summary?: Record<string, any>): Promise<void> {
    await this.client.post(`/api/calls/${callId}/end`, { summary });
  }

  // Email endpoints
  async sendFollowupEmail(email: string, subject: string, body: string): Promise<void> {
    await this.client.post('/api/emails/send-followup', {
      recipient_email: email,
      subject,
      body,
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiService = new APIService();
