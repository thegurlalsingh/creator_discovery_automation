import React, { useState, useEffect, useRef } from "react";
import Header from "./components/Header";
import Instructions from "./components/Instructions";
import PipelineTab from "./components/PipelineTab";
import DatabaseTab from "./components/DatabaseTab";
import OutreachTab from "./components/OutreachTab";

const API_BASE = "http://https://creator-discovery-automation.onrender.com/api";

export default function App() {
  const [activeTab, setActiveTab] = useState("pipeline"); 
  const [activeDbTab, setActiveDbTab] = useState("creators"); 
  
  const [isRunning, setIsRunning] = useState(false);
  const [isStopping, setIsStopping] = useState(false);
  const [logs, setLogs] = useState([]);
  
  const [keywordsInput, setKeywordsInput] = useState("yoga, wellness, fashion, technology");
  const [peopleCountInput, setPeopleCountInput] = useState(5);
  
  const [creators, setCreators] = useState([]);
  const [reels, setReels] = useState([]);
  const [outreachData, setOutreachData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const [emailStatusMsg, setEmailStatusMsg] = useState("");
  const [sendingId, setSendingId] = useState(null);

  const terminalEndRef = useRef(null);

  const checkStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/status`);
      const data = await res.json();
      setIsRunning(data.running);
      if (!data.running) {
        setIsStopping(false);
      }
    } catch (err) {
      console.error("Failed to connect to backend:", err);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let eventSource = null;

    if (isRunning) {
      eventSource = new EventSource(`${API_BASE}/stream`);
      
      eventSource.onmessage = (event) => {
        setLogs((prev) => {
          if (event.data === "\n" && prev[prev.length - 1] === "") {
            return prev;
          }
          return [...prev, event.data];
        });
      };

      eventSource.onerror = (err) => {
        console.error("EventSource failed:", err);
        eventSource.close();
      };
    }

    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [isRunning]);

  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const fetchDbData = async () => {
    setIsLoading(true);
    setErrorMsg("");
    try {
      const [creatorsRes, reelsRes, outreachRes] = await Promise.all([
        fetch(`${API_BASE}/db/creators`).then(r => r.json()),
        fetch(`${API_BASE}/db/reels`).then(r => r.json()),
        fetch(`${API_BASE}/db/outreach`).then(r => r.json())
      ]);
      setCreators(creatorsRes);
      setReels(reelsRes);
      setOutreachData(outreachRes);
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to query records from Supabase database proxy.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === "database" || activeTab === "outreach") {
      fetchDbData();
    }
  }, [activeTab]);

  const handleStartPipeline = async () => {
    const count = parseInt(peopleCountInput, 10);
    if (isNaN(count) || count < 1 || count > 50) {
      setLogs((prev) => [...prev, `\n[SYSTEM ERROR]: Search people count must be a number between 1 and 50.\n`]);
      return;
    }

    setLogs(["[SYSTEM]: Initiating startup requests...", "\n"]);
    try {
      const body = {
        keywords: keywordsInput,
        target_profiles: count
      };

      const res = await fetch(`${API_BASE}/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error running scraper");
      }
      setIsRunning(true);
    } catch (err) {
      setLogs((prev) => [...prev, `\n[SYSTEM ERROR]: ${err.message}\n`]);
    }
  };

  const handleStopPipeline = async () => {
    setIsStopping(true);
    setLogs((prev) => [...prev, "\n[SYSTEM]: Requesting pipeline stoppage...\n"]);
    try {
      const res = await fetch(`${API_BASE}/stop`, { method: "POST" });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error stopping scraper");
      }
    } catch (err) {
      setLogs((prev) => [...prev, `\n[SYSTEM ERROR]: ${err.message}\n`]);
      setIsStopping(false);
    }
  };

  const handleClearLogs = () => {
    setLogs([]);
  };

  const handleSendEmail = async (creatorId) => {
    setSendingId(creatorId);
    setEmailStatusMsg("");
    try {
      const res = await fetch(`${API_BASE}/outreach/send/${creatorId}`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to trigger email send");
      }
      setEmailStatusMsg(`Successfully sent email to creator!`);
      fetchDbData();
    } catch (err) {
      setEmailStatusMsg(`Error sending email: ${err.message}`);
    } finally {
      setSendingId(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      <Instructions />

      <main className="w-full">
        {activeTab === "pipeline" && (
          <PipelineTab
            isRunning={isRunning}
            isStopping={isStopping}
            logs={logs}
            keywordsInput={keywordsInput}
            setKeywordsInput={setKeywordsInput}
            peopleCountInput={peopleCountInput}
            setPeopleCountInput={setPeopleCountInput}
            handleStartPipeline={handleStartPipeline}
            handleStopPipeline={handleStopPipeline}
            handleClearLogs={handleClearLogs}
            terminalEndRef={terminalEndRef}
          />
        )}

        {activeTab === "database" && (
          <DatabaseTab
            activeDbTab={activeDbTab}
            setActiveDbTab={setActiveDbTab}
            creators={creators}
            reels={reels}
            outreachData={outreachData}
            isLoading={isLoading}
            errorMsg={errorMsg}
            fetchDbData={fetchDbData}
          />
        )}

        {activeTab === "outreach" && (
          <OutreachTab
            outreachData={outreachData}
            creators={creators}
            emailStatusMsg={emailStatusMsg}
            sendingId={sendingId}
            handleSendEmail={handleSendEmail}
            fetchDbData={fetchDbData}
            isLoading={isLoading}
          />
        )}
      </main>
    </div>
  );
}
