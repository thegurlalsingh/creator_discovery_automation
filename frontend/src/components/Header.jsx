import React from "react";

export default function Header({ activeTab, setActiveTab }) {
  return (
    <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-border-glass pb-6 gap-4">
      <div className="logo-section">
        <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-br from-white via-white to-accent-primary bg-clip-text text-transparent flex items-center gap-2">
          Creator Scraper 
        </h1>
        <p className="text-text-secondary text-sm mt-1">
          Automate discovery, analyze performance, and trigger outbound outreach campaigns
        </p>
      </div>
      <div className="flex gap-1.5 bg-bg-secondary p-1.5 rounded-lg border border-border-glass w-fit">
        <button
          className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 flex items-center gap-2 cursor-pointer ${
            activeTab === "pipeline"
              ? "text-white bg-bg-tertiary shadow-lg"
              : "text-text-secondary hover:text-white hover:bg-white/5"
          }`}
          onClick={() => setActiveTab("pipeline")}
        >
          Scraper Run
        </button>
        <button
          className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 flex items-center gap-2 cursor-pointer ${
            activeTab === "database"
              ? "text-white bg-bg-tertiary shadow-lg"
              : "text-text-secondary hover:text-white hover:bg-white/5"
          }`}
          onClick={() => setActiveTab("database")}
        >
          Database Tables
        </button>
        <button
          className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 flex items-center gap-2 cursor-pointer ${
            activeTab === "outreach"
              ? "text-white bg-bg-tertiary shadow-lg"
              : "text-text-secondary hover:text-white hover:bg-white/5"
          }`}
          onClick={() => setActiveTab("outreach")}
        >
          Outreach Dashboard
        </button>
      </div>
    </header>
  );
}
