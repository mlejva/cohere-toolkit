import { useQuery } from '@tanstack/react-query';

import { ManagedTool, useCohereClient } from '@/cohere-client';
import { ToolOutput } from '@/components/MessageContent';

export const useListTools = (enabled: boolean = true) => {
  const client = useCohereClient();
  return useQuery<ManagedTool[], Error>({
    queryKey: ['tools'],
    queryFn: async () => {
      return await client.listTools({});
    },
    refetchOnWindowFocus: false,
    enabled,
  });
};

export const useListToolOutputs = (conversationId: string | undefined = "", enabled: boolean = true) => {
  const client = useCohereClient();

  const result = useQuery<ToolOutput[], Error>({
    queryKey: ['tools'],
    queryFn: async () => {
      return await client.toolOutputConversationsConversationIdToolOutputsGet({ conversationId });
    },
    refetchOnWindowFocus: false,
    enabled,
    refetchInterval: 1000,
    refetchOnMount: true,
    refetchOnReconnect: true,
    refetchIntervalInBackground: true,
  });

  return conversationId ? result : {
    data: [],
    isLoading: false,
    isError: false,
  }
};
