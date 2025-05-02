import { useState } from "react";

function App() {
    const [count, setCount] = useState(0);

    return (
        <Worker
            id={1}
            name="Worker 1"
            is_working={true}
            current_activity="Boning"
            should_sharpen={false}
        />
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
        <div className=" border-2 border-slate-950 rounded-2xl">
            <div className="w-3xs aspect-square bg-amber-300"></div>
        </div>
    );
};

export default App;
