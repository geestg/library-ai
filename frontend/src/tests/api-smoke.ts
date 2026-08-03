import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
});

async function run() {
    console.log("");
    console.log("====================================");
    console.log("DELBOT API SMOKE TEST");
    console.log("====================================");

    try {
        const health = await api.get("/health");

        console.log("");
        console.log("[OK] HEALTH");
        console.log(health.data);
    } catch (e: any) {
        console.log("");
        console.log("[FAILED] HEALTH");
        console.log(e.message);
    }

    try {
        const root = await api.get("/");

        console.log("");
        console.log("[OK] ROOT");
        console.log(root.data);
    } catch (e: any) {
        console.log("");
        console.log("[FAILED] ROOT");
        console.log(e.message);
    }

    try {
        const repository = await api.get("/repository/explorer");

        console.log("");
        console.log("[OK] REPOSITORY");
        console.log(repository.data);
    } catch (e: any) {
        console.log("");
        console.log("[FAILED] REPOSITORY");
        console.log(e.message);
    }

    console.log("");
    console.log("====================================");
    console.log("FINISHED");
    console.log("====================================");
}

run();
