import { Card } from "./ui/card";
import { Clock } from "lucide-react";

interface Activity {
  id: string;
  title: string;
  location: string;
  time: string;
  risk: "Red" | "Amber" | "Green";
  description: string;
}

export default function RecentActivity() {
  const activities: Activity[] = [
    {
      id: "INC-29857",
      title: "Dropped Pry Bar",
      location: "Offshore Platform A",
      time: "2 hours ago",
      risk: "Red",
      description: "Tool fell from elevated work area during maintenance",
    },
    {
      id: "INC-29856",
      title: "Near Miss - Valve Pressure",
      location: "Subsea Unit 3",
      time: "5 hours ago",
      risk: "Amber",
      description: "Pressure valve reading exceeded normal threshold",
    },
    {
      id: "INC-29855",
      title: "Safety Compliance Check",
      location: "Processing Facility B",
      time: "8 hours ago",
      risk: "Green",
      description: "Routine inspection completed successfully",
    },
    {
      id: "INC-29854",
      title: "Equipment Malfunction",
      location: "Pipeline Section 12",
      time: "1 day ago",
      risk: "Amber",
      description: "Sensor malfunction detected during routine check",
    },
    {
      id: "INC-29853",
      title: "Minor Injury - Hand Laceration",
      location: "Workshop C",
      time: "1 day ago",
      risk: "Red",
      description: "Worker sustained cut while handling equipment",
    },
    {
      id: "INC-29852",
      title: "Safety Training Completed",
      location: "Training Center",
      time: "2 days ago",
      risk: "Green",
      description: "Quarterly safety certification for 24 personnel",
    },
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "Red":
        return "bg-red-500";
      case "Amber":
        return "bg-amber-500";
      case "Green":
        return "bg-green-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <Card className="p-6 shadow-sm border-gray-200">
      <div className="mb-4">
        <h2 className="font-semibold text-gray-900">Recent Activity</h2>
        <p className="text-sm text-gray-500">Latest safety incidents and events</p>
      </div>

      <div className="space-y-3">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer"
          >
            <div className="flex items-start gap-3">
              <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${getRiskColor(activity.risk)}`} />
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <h3 className="font-medium text-gray-900 text-sm">{activity.title}</h3>
                  <span className="text-xs text-gray-500 whitespace-nowrap">{activity.id}</span>
                </div>
                <p className="text-xs text-gray-600 mb-1">{activity.description}</p>
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <span>{activity.location}</span>
                  <span>•</span>
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{activity.time}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
