export function parseCitations(

  text,

  onCitationClick

) {

  const parts = text.split(

    /(\[\d+\])/g

  );

  return parts.map(

    (
      part,
      index
    ) => {

      const match = part.match(

        /\[(\d+)\]/

      );

      if (!match) {

        return (

          <span key={index}>

            {part}

          </span>

        );

      }

      const citationId = Number(

        match[1]

      );

      return (

        <button

          key={index}

          className="inline-citation"

          onClick={() =>

            onCitationClick?.(
              citationId
            )

          }

        >

          [{citationId}]

        </button>

      );

    }

  );

}

export const renderCitationText = parseCitations;