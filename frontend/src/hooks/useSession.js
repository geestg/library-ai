import {
  useEffect,
  useState,
} from "react";

import {

  createSession,

} from "../services/sessionApi";

const STORAGE_KEY =
  "workspace_session_id";

export default function useSession() {

  const [

    sessionId,

    setSessionId,

  ] = useState(null);

  useEffect(() => {

    async function initialize() {

      const stored =

        localStorage.getItem(

          STORAGE_KEY

        );

      if (stored) {

        setSessionId(

          stored

        );

        return;

      }

      const session =

        await createSession();

      localStorage.setItem(

        STORAGE_KEY,

        session.session_id

      );

      setSessionId(

        session.session_id

      );

    }

    initialize();

  }, []);

  return {

    sessionId,

  };

}