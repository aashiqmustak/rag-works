import { useState, useCallback } from 'react';
import { apiService } from '@/services/api';
import { useConversationStore } from '@/store';
import type { ChatMessage, ChatResponse } from '@/types';
import { v4 as uuidv4 } from 'uuid';

export const useChat = () => {
  const [loading, setLoading] = useState(false);
  const { addMessage, setError, setInsights, setProperties } =
    useConversationStore();
  const leadId = useConversationStore((state) => state.leadId);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!leadId || !content.trim()) return;

      setLoading(true);
      setError(null);

      try {
        // Add user message
        const userMessage: ChatMessage = {
          id: uuidv4(),
          lead_id: leadId,
          role: 'user',
          content,
          timestamp: new Date().toISOString(),
        };
        addMessage(userMessage);

        // Get response
        const response: ChatResponse = await apiService.sendMessage(
          leadId,
          content
        );

        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: uuidv4(),
          lead_id: leadId,
          role: 'assistant',
          content: response.response,
          timestamp: new Date().toISOString(),
        };
        addMessage(assistantMessage);

        // Update state
        if (response.properties_recommended) {
          setProperties(response.properties_recommended);
        }
        if (response.lead_insights) {
          setInsights(response.lead_insights);
        }
      } catch (error) {
        setError(
          error instanceof Error ? error.message : 'Failed to send message'
        );
      } finally {
        setLoading(false);
      }
    },
    [leadId, addMessage, setError, setInsights, setProperties]
  );

  return { sendMessage, loading };
};
