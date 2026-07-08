import {
  forwardRef,
} from "react";

import ChatHero from "../chat/ChatHero";
import MessageBubble from "../chat/MessageBubble";
import ThinkingIndicator from "../chat/ThinkingIndicator";

import {
  ConversationState,
} from "../../hooks/useConversationState";

const SessionConversation =
  forwardRef(function SessionConversation({

    messages = [],

    conversationState,

    sources = [],

    setInput,

    setSelectedThesis,

    setActiveCitation,

    onScroll,

  }, ref) {

    // =====================================
    // STATE
    // =====================================

    const isThinking =

      conversationState ===

      ConversationState.THINKING;

    const hasMessages =

      messages.length > 0;

    // =====================================
    // UI
    // =====================================

    return (

      <div

        ref={ref}

        className={`modern-messages ${

          !hasMessages

            ? "empty-chat"

            : "has-messages"

        }`}

        onScroll={onScroll}

      >

        <div className="conversation-content">

          {

            !hasMessages

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
                          msg.id ||
                          `${msg.role}-${idx}`
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

          <div

            className="conversation-bottom-anchor"

            aria-hidden="true"

          />

        </div>

      </div>

    );

  });

export default SessionConversation;