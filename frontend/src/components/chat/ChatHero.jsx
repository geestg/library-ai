const starterPrompts = [

  {
    label:
      "Temukan celah penelitian",

    prompt:
      "Bantu saya menemukan celah penelitian dari topik yang ingin saya teliti.",
  },

  {
    label:
      "Bandingkan metode",

    prompt:
      "Bandingkan metode penelitian yang relevan untuk topik saya.",
  },

  {
    label:
      "Analisis dokumen",

    prompt:
      "Analisis dokumen yang saya lampirkan dan jelaskan temuan utamanya.",
  },

];

export default function ChatHero({

  setInput,

}) {

  // =====================================
  // SELECT STARTER PROMPT
  // =====================================

  const handlePromptSelect =
    (prompt) => {

      setInput?.(
        prompt
      );

    };

  // =====================================
  // UI
  // =====================================

  return (

    <section

      className="hero-section"

      aria-labelledby="hero-title"

    >

      {/* ================================= */}
      {/* INTRO */}
      {/* ================================= */}

      <div className="hero-intro">

        <h1 id="hero-title">

          <span>

            Academic Research

          </span>

          <span>

            Intelligence

          </span>

        </h1>

        <p>

          Mulai dari pertanyaan penelitian,
          metode yang ingin dibandingkan,
          atau dokumen yang perlu dianalisis.

        </p>

      </div>

      {/* ================================= */}
      {/* STARTER PROMPTS */}
      {/* ================================= */}

      <div

        className="hero-starter-prompts"

        aria-label="Saran pertanyaan awal"

      >

        {

          starterPrompts.map(

            (item) => (

              <button

                key={
                  item.label
                }

                type="button"

                className="hero-starter-button"

                onClick={() =>

                  handlePromptSelect(
                    item.prompt
                  )

                }

              >

                {item.label}

              </button>

            )

          )

        }

      </div>

    </section>

  );

}