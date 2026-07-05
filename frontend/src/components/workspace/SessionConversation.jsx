import ChatHero from "../chat/ChatHero";
import MessageBubble from "../chat/MessageBubble";
import ThinkingIndicator from "../chat/ThinkingIndicator";

import {
  ConversationState,
} from "../../hooks/useConversationState";

export default function SessionConversation({

  messages = [],

  conversationState,

  sources = [],

  setInput,

  setSelectedThesis,

  setActiveCitation,

}) {

  // =====================================
  // STATE
  // =====================================

  const isThinking =

    conversationState ===

    ConversationState.THINKING;

  // =====================================
  // UI
  // =====================================

  return (

    <div

      className={`modern-messages ${

        messages.length === 0

          ? "empty-chat"

          : ""

      }`}

    >
          {

        messages.length === 0

          ? (

              <ChatHero

                setInput={
                  setInput
                }

              />

            )

          : (

              messages.map(

                (

                  msg,

                  idx

                ) => (

                  <MessageBubble

                    key={
                      msg.id || idx
                    }

                    role={
                      msg.role
                    }

                    content={
                      msg.content
                    }

                    citations={
                      msg.citations
                    }

                    evidence={
                      msg.evidence
                    }

                    noveltyAnalysis={
                      msg.noveltyAnalysis
                    }

                    attachedDocuments={
                      msg.attachedDocuments
                    }

                    sources={
                      sources
                    }

                    setSelectedThesis={
                      setSelectedThesis
                    }

                    setActiveCitation={
                      setActiveCitation
                    }

                  />

                )

              )

            )

      }
            {

        isThinking && (

          <ThinkingIndicator />

        )

      }

    </div>

  );

}