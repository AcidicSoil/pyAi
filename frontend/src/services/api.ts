const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface Agent {
  name: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  description: string;
  lastActive?: string;
}

export const agentApi = {
  listAgents: async (): Promise<Agent[]> => {
    const response = await fetch(`${API_BASE_URL}/agents`);
    if (!response.ok) {
      throw new Error('Failed to fetch agents');
    }
    const data = await response.json();
    return data.map((agent: any) => ({
      ...agent,
      lastActive: agent.last_active,
    }));
  },

  getAgent: async (name: string): Promise<Agent> => {
    const response = await fetch(`${API_BASE_URL}/agents/${name}`);
    if (!response.ok) {
      throw new Error('Failed to fetch agent');
    }
    const data = await response.json();
    return {
      ...data,
      lastActive: data.last_active,
    };
  },

  createTask: async (agentName: string, task: any): Promise<any> => {
    const response = await fetch(`${API_BASE_URL}/agents/${agentName}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });
    if (!response.ok) {
      throw new Error('Failed to create task');
    }
    return response.json();
  },
};
