import React from "react";

export default function PipelineTab({
  isRunning,
  isStopping,
  logs,
  keywordsInput,
  setKeywordsInput,
  peopleCountInput,
  setPeopleCountInput,
  handleStartPipeline,
  handleStopPipeline,
  handleClearLogs,
  terminalEndRef
}) {
  return (
    <div className="bg-bg-glass backdrop-blur-md border border-border-glass rounded-xl shadow-main p-6 transition-all duration-200 hover:border-white/12 flex flex-col gap-4">
      <div className="flex flex-wrap gap-6 p-4 bg-white/2 rounded-lg border border-border-glass mb-2">
        <div className="flex flex-col gap-1.5 flex-1 min-w-[280px]">
          <label className="text-xs font-semibold text-text-secondary block">
            Keywords (comma-separated)
          </label>
          <input
            type="text"
            value={keywordsInput}
            onChange={(e) => setKeywordsInput(e.target.value)}
            disabled={isRunning}
            className="bg-bg-secondary border border-border-glass rounded-md text-white px-3.5 py-2 text-sm outline-none font-sans focus:border-accent-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            placeholder="e.g. yoga, wellness, fashion"
          />
        </div>
        <div className="flex flex-col gap-1.5 w-full md:w-[160px]">
          <label className="text-xs font-semibold text-text-secondary block">
            Search Count (Max 50)
          </label>
          <input
            type="number"
            min="1"
            max="50"
            value={peopleCountInput}
            onChange={(e) => setPeopleCountInput(e.target.value)}
            disabled={isRunning}
            className="bg-bg-secondary border border-border-glass rounded-md text-white px-3.5 py-2 text-sm outline-none font-mono focus:border-accent-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>
      </div>

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Pipeline Terminal</h3>
          <p className="text-xs text-text-secondary mt-1">
            Status:{" "}
            <span
              className={`font-semibold ${
                isRunning ? "text-accent-primary" : "text-accent-warning"
              }`}
            >
              {isRunning ? "Scraping Pipeline Running" : "○ Idle"}
            </span>
          </p>
        </div>
        <div className="flex gap-2">
          {isRunning ? (
            <button
              className="bg-accent-danger text-white border-none px-4 py-2 rounded-md font-semibold cursor-pointer flex items-center gap-2 transition-all duration-200 hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              onClick={handleStopPipeline}
              disabled={isStopping}
            >
              {isStopping ? "Stopping..." : "Stop Scraper Pipeline"}
            </button>
          ) : (
            <button
              className="bg-accent-primary text-black font-bold border-none px-4 py-2 rounded-md cursor-pointer flex items-center gap-2 transition-all duration-200 shadow-md shadow-accent-primary/40 hover:bg-emerald-600 hover:-translate-y-[1px] hover:shadow-lg hover:shadow-accent-primary/50 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              onClick={handleStartPipeline}
              disabled={isRunning}
            >
              Start Scraper Pipeline
            </button>
          )}
          <button
            className="bg-bg-tertiary border border-border-glass text-white px-4 py-2 rounded-md font-medium cursor-pointer flex items-center gap-2 transition-all duration-200 hover:bg-white/5 hover:border-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            onClick={handleClearLogs}
            disabled={logs.length === 0}
          >
            Clear Screen
          </button>
        </div>
      </div>

      <div className="flex flex-col h-[480px] bg-[#040508] border border-border-glass rounded-xl overflow-hidden shadow-main">
        <div className="bg-[#0f111a] px-4 py-3 flex justify-between items-center border-b border-border-glass">
          <div className="flex gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#ff5f56]"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-[#ffbd2e]"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-[#27c93f]"></span>
          </div>
          <div className="font-mono text-xs text-text-secondary flex items-center gap-1.5">
            bash - log_streamer.py - 8000
          </div>
        </div>
        <div className="grow p-5 overflow-y-auto font-mono text-[13px] leading-relaxed text-gray-300">
          {logs.map((log, idx) => (
            <div key={idx} className="whitespace-pre-wrap break-all mb-1">
              {log}
            </div>
          ))}
          {isRunning && (
            <div className="whitespace-pre-wrap break-all mb-1">
              <span className="inline-block w-2 h-3.5 bg-accent-primary ml-1 align-middle terminal-cursor-blink"></span>
            </div>
          )}
          {logs.length === 0 && !isRunning && (
            <div className="whitespace-pre-wrap break-all mb-1 text-text-muted">
              Console idle. Click "Start Scraper Pipeline" to kick off the background job.
            </div>
          )}
          <div ref={terminalEndRef} />
        </div>
      </div>
    </div>
  );
}
