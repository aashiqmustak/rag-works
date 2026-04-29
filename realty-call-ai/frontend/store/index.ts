import { create } from 'zustand';
import type { ChatMessage, LeadInsight, Property, Lead } from '@/types';

interface ConversationState {
  leadId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  leadInsights: LeadInsight | null;
  recommendedProperties: Property[];
  lead: Lead | null;

  setLeadId: (leadId: string) => void;
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setInsights: (insights: LeadInsight | null) => void;
  setProperties: (properties: Property[]) => void;
  setLead: (lead: Lead | null) => void;
  clearMessages: () => void;
}

export const useConversationStore = create<ConversationState>((set) => ({
  leadId: null,
  messages: [],
  isLoading: false,
  error: null,
  leadInsights: null,
  recommendedProperties: [],
  lead: null,

  setLeadId: (leadId: string) => set({ leadId }),
  addMessage: (message: ChatMessage) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
  setInsights: (insights: LeadInsight | null) => set({ leadInsights: insights }),
  setProperties: (properties: Property[]) =>
    set({ recommendedProperties: properties }),
  setLead: (lead: Lead | null) => set({ lead }),
  clearMessages: () => set({ messages: [], leadInsights: null }),
}));

interface CallState {
  callId: string | null;
  isInCall: boolean;
  callStatus: string;
  callStartTime: number | null;

  setCallId: (callId: string) => void;
  setInCall: (inCall: boolean) => void;
  setCallStatus: (status: string) => void;
  setCallStartTime: (time: number) => void;
  endCall: () => void;
}

export const useCallStore = create<CallState>((set) => ({
  callId: null,
  isInCall: false,
  callStatus: 'idle',
  callStartTime: null,

  setCallId: (callId: string) => set({ callId }),
  setInCall: (inCall: boolean) => set({ isInCall: inCall }),
  setCallStatus: (status: string) => set({ callStatus: status }),
  setCallStartTime: (time: number) => set({ callStartTime: time }),
  endCall: () => set({ callId: null, isInCall: false, callStatus: 'idle', callStartTime: null }),
}));
