import { useState } from "react";

function App() {
    const [count, setCount] = useState(0);

    return (
        <div className="p-2 gap-2 flex">
            <Worker
                id={1}
                name="Worker 1"
                is_working={true}
                current_activity="Boning"
                should_sharpen={false}
            />
            <Worker
                id={1}
                name="Worker 1"
                is_working={true}
                current_activity="Boning"
                should_sharpen={false}
            />
            <Worker
                id={1}
                name="Worker 1"
                is_working={true}
                current_activity="Boning"
                should_sharpen={false}
            />
            <Worker
                id={1}
                name="Worker 1"
                is_working={true}
                current_activity="Boning"
                should_sharpen={false}
            />
        </div>
    );
}

export const activityTypes = ["Boning", "Slicing"] as const;
export type ActivityTypes = (typeof activityTypes)[number];

const Worker = (props: {
    id: number;
    name: string;
    is_working: boolean;
    current_activity: ActivityTypes;
    should_sharpen: boolean;
}) => {
    return (
        <div className=" border-2 border-slate-950 rounded-2xl p-3">
            <div className="relative rounded-full w-3xs aspect-square bg-amber-300 border-2 border-slate-900">
                <div className="w-full h-full flex items-center justify-center">
                    <svg
                        className="w-4/5 h-4/5"
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        fill="#000000"
                        viewBox="0 0 256 256"
                    >
                        <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                    </svg>
                </div>

                {props.is_working ? (
                    <div className="absolute bottom-7 right-7 bg-green-600 w-5 h-5 rounded-full border-2 border-slate-900"></div>
                ) : (
                    <div className="absolute bottom-7 right-7 bg-red-600 w-5 h-5 rounded-full border-2 border-slate-900"></div>
                )}
            </div>
            <div>ID: {props.id}</div>
            <div>Name: {props.name}</div>
            <div>Current Activity: {props.current_activity}</div>
            <div>Should Sharpen: {props.should_sharpen ? "Yes" : "No"}</div>
        </div>
    );
};

export default App;
