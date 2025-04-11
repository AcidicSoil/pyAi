import React, { useEffect, useState } from 'react';
import AgentCard from '../components/agents/AgentCard';
import Layout from '../components/layout/Layout';
import { Agent, agentApi } from '../services/api';

const Home: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await agentApi.listAgents();
        setAgents(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch agents:', err);
        setError('Failed to load agents. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  return (
    <Layout>
      <div className="space-y-6">
        <h2 className="text-3xl font-bold">Welcome to AI Agent Framework</h2>
        <p className="text-gray-600">
          A modular, Python-based AI agent system focused on autonomous research,
          collaboration, and extensibility.
        </p>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading agents...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-800">
            {error}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <AgentCard key={agent.name} {...agent} />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Home;
