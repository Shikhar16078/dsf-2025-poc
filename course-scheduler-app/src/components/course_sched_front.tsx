// import { useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Textarea } from "@/components/ui/textarea";
// import { Input } from "@/components/ui/input";
// import { Card, CardContent } from "@/components/ui/card";

// export default function CourseScheduler() {
//   const [eligibleCourses, setEligibleCourses] = useState("CS 141\nCS 150\nSTAT 155\nMATH 010A\nPHYS 040A");
//   const [response, setResponse] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async () => {
//     setLoading(true);
//     setResponse("");

//     const formattedCourses = eligibleCourses
//       .split("\n")
//       .map((line) => `- ${line.trim()}`)
//       .join("\n");

//     const prompt = `I am a computer science student. These are the courses I'm eligible to take this quarter:\n\n${formattedCourses}\n\nPlease help me build a suggested schedule using 3–5 of these classes. I prefer a balanced workload and want to satisfy core requirements first. Please explain your choices briefly.`;

//     const payload = {
//       contents: [
//         {
//           parts: [{ text: prompt }],
//         },
//       ],
//     };

//     try {
//       const res = await fetch(
//         "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=YOUR_API_KEY",
//         {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify(payload),
//         }
//       );

//       if (!res.ok) {
//         throw new Error(`API Error: ${res.status}`);
//       }

//       const data = await res.json();
//       const text =
//         data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response.";
//       setResponse(text);
//     } catch (err) {
//       setResponse(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="p-6 max-w-2xl mx-auto space-y-4">
//       <Card>
//         <CardContent className="p-4">
//           <h1 className="text-xl font-bold mb-2">Course Scheduler</h1>
//           <Textarea
//             className="w-full mb-4"
//             rows={8}
//             value={eligibleCourses}
//             onChange={(e) => setEligibleCourses(e.target.value)}
//             placeholder="Enter eligible courses, one per line (e.g. CS 141)"
//           />
//           <Button onClick={handleSubmit} disabled={loading}>
//             {loading ? "Generating..." : "Generate Schedule"}
//           </Button>
//         </CardContent>
//       </Card>

//       {response && (
//         <Card>
//           <CardContent className="p-4 whitespace-pre-wrap">
//             <h2 className="text-lg font-semibold mb-2">Suggested Schedule</h2>
//             {response}
//           </CardContent>
//         </Card>
//       )}
//     </div>
//   );
// }


import { useState } from "react";

export default function CourseScheduler() {
  const [eligibleCourses, setEligibleCourses] = useState(
    "CS 141\nCS 150\nSTAT 155\nMATH 010A\nPHYS 040A"
  );
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResponse("");

    const formattedCourses = eligibleCourses
      .split("\n")
      .map((line) => `- ${line.trim()}`)
      .join("\n");

    const prompt = `I am a computer science student. These are the courses I'm eligible to take this quarter:\n\n${formattedCourses}\n\nPlease help me build a suggested schedule using 3–5 of these classes. I prefer a balanced workload and want to satisfy core requirements first. Please explain your choices briefly.`;

    const payload = {
      contents: [
        {
          parts: [{ text: prompt }],
        },
      ],
    };

    try {
      const res = await fetch(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=API_KEY_HERE",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      if (!res.ok) throw new Error(`API Error: ${res.status}`);

      const data = await res.json();
      const text = data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response.";
      setResponse(text);
    } catch (err: any) {
      setResponse(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-4">
      <div className="border p-4 rounded shadow">
        <h1 className="text-xl font-bold mb-2">Course Scheduler</h1>
        <textarea
          className="w-full mb-4 border p-2 rounded"
          rows={8}
          value={eligibleCourses}
          onChange={(e) => setEligibleCourses(e.target.value)}
          placeholder="Enter eligible courses, one per line (e.g. CS 141)"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          {loading ? "Generating..." : "Generate Schedule"}
        </button>
      </div>

      {response && (
        <div className="border p-4 rounded shadow whitespace-pre-wrap">
          <h2 className="text-lg font-semibold mb-2">Suggested Schedule</h2>
          {response}
        </div>
      )}
    </div>
  );
}