import { ToolOutput } from '@/components/MessageContent';

interface Props {
  toolOutputs?: ToolOutput[];
}

function ToolContent({ toolOutputs = [] }: Props) {
  return (
    <>
      {toolOutputs.map((output, index) => (
        <div key={index} className="flex flex-col gap-2 w-full">
          {output.outputs.map(r =>
            r.results.map(r =>
              <>
                {
                  r.type === 'image/png' && (
                    <img
                      key={index}
                      src={`data:image/png;base64,${r.data}`}
                      alt="Tool output"
                      className="w-full flex flex-1"
                    />
                  )
                }
              </>
            )
          )}
        </div>
      ))}
    </>
  )
}

export default ToolContent;
