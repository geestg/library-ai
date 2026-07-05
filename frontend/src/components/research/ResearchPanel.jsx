import ResearchSummaryCard from "./ResearchSummaryCard";
import NoveltyWidget from "./NoveltyWidget";
import TrendWidget from "./TrendWidget";
import GapWidget from "./GapWidget";
import CompetencyWidget from "./CompetencyWidget";
import ProdiWidget from "./ProdiWidget";
import RelatedThesisWidget from "./RelatedThesisWidget";

export default function ResearchPanel({

  researchProfile,

  sources = [],

  activeCitation,

  setActiveCitation,

  setSelectedThesis

}) {

  return (

    <div className="research-panel">

      <ResearchSummaryCard

        researchProfile={researchProfile}

        sourceCount={sources.length}

      />

      <NoveltyWidget

        novelty={

          researchProfile?.novelty

        }

      />

      <TrendWidget

        trend={

          researchProfile?.trend

        }

      />

      <GapWidget

        gap={

          researchProfile?.gap

        }

      />

      <CompetencyWidget

        competency={

          researchProfile?.competency

        }

      />

      <ProdiWidget

        prodi={

          researchProfile?.prodi

        }

      />

      <RelatedThesisWidget

        sources={sources}

        activeCitation={activeCitation}

        setActiveCitation={

          setActiveCitation

        }

        setSelectedThesis={

          setSelectedThesis

        }

      />

    </div>

  );

}