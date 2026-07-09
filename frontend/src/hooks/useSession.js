import {
  useEffect,
  useState,
} from "react";

import {

  createSession,

  getSession,

} from "../services/sessionApi";

const STORAGE_KEY =
  "workspace_session_id";

export default function useSession() {

  // =====================================
  // SESSION
  // =====================================

  const [

    sessionId,

    setSessionId,

  ] = useState(null);

  // =====================================
  // SESSION INITIALIZATION
  // =====================================

  useEffect(() => {

    let cancelled = false;

    async function initialize() {

      const storedSessionId =

        localStorage.getItem(

          STORAGE_KEY

        );

      // =================================
      // VALIDATE STORED SESSION
      // =================================

      if (storedSessionId) {

        try {

          const session =

            await getSession({

              sessionId:
                storedSessionId,

            });

          if (cancelled) {

            return;

          }

          localStorage.setItem(

            STORAGE_KEY,

            session.session_id

          );

          setSessionId(

            session.session_id

          );

          console.info(

            "[SESSION RESTORED]",

            session.session_id

          );

          return;

        }

        catch (error) {

          if (cancelled) {

            return;

          }

          console.warn(

            "[SESSION RESTORE FAILED]",

            {

              sessionId:
                storedSessionId,

              status:
                error?.response?.status,

            }

          );

          localStorage.removeItem(

            STORAGE_KEY

          );

        }

      }

      // =================================
      // CREATE REPLACEMENT SESSION
      // =================================

      try {

        const session =

          await createSession();

        if (cancelled) {

          return;

        }

        localStorage.setItem(

          STORAGE_KEY,

          session.session_id

        );

        setSessionId(

          session.session_id

        );

        console.info(

          "[SESSION CREATED]",

          session.session_id

        );

      }

      catch (error) {

        if (cancelled) {

          return;

        }

        console.error(

          "[SESSION INITIALIZATION FAILED]",

          error

        );

      }

    }

    initialize();

    return () => {

      cancelled = true;

    };

  }, []);

  // =====================================
  // EXPORT
  // =====================================

  return {

    sessionId,

  };

}