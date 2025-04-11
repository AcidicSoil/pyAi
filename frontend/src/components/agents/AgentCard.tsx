import React from 'react';

interface AgentCardProps {
  name: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  description: string;
  lastActive?: string;
}

const AgentCard: React.FC<AgentCardProps> = ({
  name,
  status,
  description,
  lastActive,
}) => {
  const statusColors = {
    idle: 'bg-gray-100 text-gray-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold">{name}</h3>
        <span className={`px-2 py-1 rounded-full text-sm ${statusColors[status]}`}>
          {status}
        </span>
      </div>
      <p className="text-gray-600 mb-4">{description}</p>
      {lastActive && (
        <p className="text-sm text-gray-500">
          Last active: {lastActive}
        </p>
      )}
    </div>
  );
};

export default AgentCard;
