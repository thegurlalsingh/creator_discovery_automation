import React from "react";

export default function Instructions() {
  return (
    <section className="bg-bg-glass backdrop-blur-md border border-border-glass rounded-xl shadow-main p-6 transition-all duration-200 hover:border-white/12">
      <h3 className="text-lg font-semibold text-white"> Instructions & Setup</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div className="flex gap-4 bg-white/2 p-4 rounded-lg border border-white/3">
          <div className="font-bold text-accent-primary bg-accent-primary-dim w-7 h-7 rounded-full flex items-center justify-center text-sm shrink-0">
            1
          </div>
          <div className="step-content">
            <h4 className="text-base font-semibold text-white mb-1">Setup Environment</h4>
            <p className="text-text-secondary text-xs md:text-sm leading-relaxed">
              Configure keywords, target count, and credentials in the backend `.env` variables.
            </p>
          </div>
        </div>
        <div className="flex gap-4 bg-white/2 p-4 rounded-lg border border-white/3">
          <div className="font-bold text-accent-primary bg-accent-primary-dim w-7 h-7 rounded-full flex items-center justify-center text-sm shrink-0">
            2
          </div>
          <div className="step-content">
            <h4 className="text-base font-semibold text-white mb-1">Run Pipeline</h4>
            <p className="text-text-secondary text-xs md:text-sm leading-relaxed">
              Press "Start Scraper Pipeline". Scraped records will auto-load into Supabase tables.
            </p>
          </div>
        </div>
        <div className="flex gap-4 bg-white/2 p-4 rounded-lg border border-white/3">
          <div className="font-bold text-accent-primary bg-accent-primary-dim w-7 h-7 rounded-full flex items-center justify-center text-sm shrink-0">
            3
          </div>
          <div className="step-content">
            <h4 className="text-base font-semibold text-white mb-1">Trigger Emails</h4>
            <p className="text-text-secondary text-xs md:text-sm leading-relaxed">
              Inspect outreach drafts on the Outreach Dashboard and click "Send Email" to trigger.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
