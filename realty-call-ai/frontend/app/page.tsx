'use client';

import React, { useState, useEffect } from 'react';
import { Phone, MessageSquare } from 'lucide-react';
import { ChatWindow } from '@/components/ChatWindow';
import { ChatInput } from '@/components/ChatInput';
import { PropertyGrid } from '@/components/PropertyCard';
import { LeadInsightPanel } from '@/components/LeadInsightPanel';
import { InitialLeadForm } from '@/components/InitialLeadForm';
import { useConversationStore, useCallStore } from '@/store';
import { useChat } from '@/hooks/useChat';
import { apiService } from '@/services/api';
import type { ChatMessage } from '@/types';
import { v4 as uuidv4 } from 'uuid';

export default function ChatPage() {
  const [showLeadForm, setShowLeadForm] = useState(true);
  const [activeTab, setActiveTab] = useState<'chat' | 'properties'>('chat');

  const {
    leadId,
    messages,
    isLoading,
    error,
    recommendedProperties,
    leadInsights,
    setLeadId,
    addMessage,
    setLoading,
  } = useConversationStore();

  const { isInCall, setInCall, setCallId } = useCallStore();
  const { sendMessage, loading } = useChat();

  const handleCreateLead = async (data: {
    name: string;
    email: string;
    phone: string;
  }) => {
    try {
      setLoading(true);
      const result = await apiService.createLead(
        data.name,
        data.email,
        data.phone
      );
      setLeadId(result.lead_id);
      setShowLeadForm(false);

      // Add welcome message
      const welcomeMsg: ChatMessage = {
        id: uuidv4(),
        lead_id: result.lead_id,
        role: 'assistant',
        content: `Hi ${data.name}! 👋 Welcome to RealtyCall AI. I'm your AI-powered real estate assistant. I'm here to help you find your perfect property! Tell me about what you're looking for - your budget, preferred location, and what type of property interests you.`,
        timestamp: new Date().toISOString(),
      };
      addMessage(welcomeMsg);
    } catch (err) {
      console.error('Error creating lead:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartVoiceCall = async () => {
    if (!leadId) return;

    try {
      setInCall(true);
      const result = await apiService.initiateCall('', leadId);
      setCallId(result.call_id);

      // Add system message
      const callMsg: ChatMessage = {
        id: uuidv4(),
        lead_id: leadId,
        role: 'assistant',
        content: '📞 Starting voice call... Please prepare to speak with your AI agent.',
        timestamp: new Date().toISOString(),
      };
      addMessage(callMsg);
    } catch (err) {
      console.error('Error starting call:', err);
      setInCall(false);
    }
  };

  if (showLeadForm) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              RealtyCall AI
            </h1>
            <p className="text-lg text-gray-600">
              Your AI-powered real estate sales assistant
            </p>
          </div>
          <InitialLeadForm onSubmit={handleCreateLead} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="text-blue-600" size={28} />
              <h1 className="text-2xl font-bold text-gray-900">
                RealtyCall AI
              </h1>
            </div>
            <button
              onClick={handleStartVoiceCall}
              disabled={isInCall}
              className="btn-primary flex items-center gap-2"
            >
              <Phone size={20} />
              {isInCall ? 'In Call...' : 'Start Voice Call'}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4 text-red-800">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Section */}
          <div className="lg:col-span-2 flex flex-col h-full">
            <div className="flex gap-2 mb-4 bg-white p-2 rounded-lg border border-gray-200">
              <button
                onClick={() => setActiveTab('chat')}
                className={`flex-1 px-4 py-2 rounded transition-colors ${
                  activeTab === 'chat'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Chat
              </button>
              <button
                onClick={() => setActiveTab('properties')}
                className={`flex-1 px-4 py-2 rounded transition-colors ${
                  activeTab === 'properties'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Properties ({recommendedProperties.length})
              </button>
            </div>

            {activeTab === 'chat' ? (
              <>
                <ChatWindow messages={messages} isLoading={loading} />
                <ChatInput
                  onSendMessage={sendMessage}
                  onStartVoiceCall={handleStartVoiceCall}
                  isLoading={loading}
                />
              </>
            ) : (
              <div className="bg-white rounded-lg shadow p-6">
                <PropertyGrid properties={recommendedProperties} />
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="flex flex-col gap-6">
            <LeadInsightPanel insights={leadInsights} />

            {/* Quick Stats */}
            <div className="card">
              <h3 className="font-bold text-gray-900 mb-4">Quick Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Messages:</span>
                  <span className="font-semibold">{messages.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Properties Viewed:</span>
                  <span className="font-semibold">
                    {recommendedProperties.length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className="font-semibold text-green-600">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
