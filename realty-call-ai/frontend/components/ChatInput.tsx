'use client';

import React, { useState } from 'react';
import { Send, Mic } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onStartVoiceCall?: () => void;
  isLoading?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onStartVoiceCall,
  isLoading = false,
}) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex gap-2 p-4 bg-white border-t border-gray-200">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={isLoading}
        className="input-base flex-1 disabled:opacity-50"
      />
      <button
        onClick={() => onStartVoiceCall?.()}
        className="btn-secondary p-2 flex items-center justify-center"
        title="Start voice call"
      >
        <Mic size={20} />
      </button>
      <button
        onClick={handleSend}
        disabled={isLoading || !input.trim()}
        className="btn-primary p-2 flex items-center justify-center disabled:opacity-50"
      >
        <Send size={20} />
      </button>
    </div>
  );
};
