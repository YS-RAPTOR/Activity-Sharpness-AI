import { useState, useEffect } from "react";

// List of activities
const activityTypes = [
    "Boning",
    "Slicing",
    "Cutting",
    "Idle",
    "Steeling",
    "Dropping",
    "Reaching",
    "Walking",
    "Placing/ Manipulating",
    "Pulling",
] as const;
type ActivityTypes = (typeof activityTypes)[number];

// Worker data
type WorkerData = {
    id: number;
    name: string;
    current_activity: ActivityTypes;
    should_sharpen: boolean;
};

function App() {
    const [workers, setWorkers] = useState<WorkerData[]>([]);

    // Fetches all workers and activity
    const fetchWorkers = async () => {
        try {
            const res = await fetch("http://localhost:8000/workers");
            const workerList = await res.json();

            const fullData = await Promise.all(
                workerList.map(async (worker: { id: number; name: string }) => {
                    const res = await fetch(`http://localhost:8000/worker/${worker.id}`);
                    const activityData = await res.json();
                    return {
                        id: worker.id,
                        name: worker.name,
                        current_activity: activityData.activity as ActivityTypes,
                        should_sharpen: activityData.should_sharpen,
                    };
                })
            );

            setWorkers(fullData);
        } catch (err) {
            console.error("Failed to load workers:", err);
        }
    };

    // Fetch once and every 10s
    useEffect(() => {
        fetchWorkers();
        const interval = setInterval(fetchWorkers, 10000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-2 gap-2 flex flex-wrap">
            {workers.map((worker) => (
                <Worker
                    key={worker.id}
                    id={worker.id}
                    name={worker.name}
                    is_working={worker.current_activity !== "Idle"}
                    current_activity={worker.current_activity}
                    should_sharpen={worker.should_sharpen}
                />
            ))}
        </div>
    );
}

const Worker = (props: {
    id: number;
    name: string;
    is_working: boolean;
    current_activity: ActivityTypes;
    should_sharpen: boolean;
}) => {
    return (
        <div className="border-2 border-slate-950 rounded-2xl p-3">
            <div className="relative rounded-full w-28 aspect-square bg-amber-300 border-2 border-slate-900">
                <div className="w-full h-full flex items-center justify-center">
                    <svg
                        className="w-4/5 h-4/5"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="#000000"
                        viewBox="0 0 256 256"
                    >
                        <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                    </svg>
                </div>
                <div
                    className={`absolute bottom-2 right-2 w-5 h-5 rounded-full border-2 border-slate-900 ${
                        props.is_working ? "bg-green-600" : "bg-red-600"
                    }`}
                ></div>
            </div>
            <div><strong>ID:</strong> {props.id}</div>
            <div><strong>Name:</strong> {props.name}</div>
            <div><strong>Current Activity:</strong> {props.current_activity}</div>
            <div><strong>Should Sharpen:</strong> {props.should_sharpen ? "Yes" : "No"}</div>
        </div>
    );
};

export default App;