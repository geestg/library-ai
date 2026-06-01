import ReactMarkdown from "react-markdown";

export default function MessageBubble({

  role,
  content

}) {

  return (

    <div className={`message ${role}`}>

      <div className="message-content">

        <ReactMarkdown>

          {content}

        </ReactMarkdown>

      </div>

    </div>

  );
}