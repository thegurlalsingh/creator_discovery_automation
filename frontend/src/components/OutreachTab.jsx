import React from "react";

export default function OutreachTab({
  outreachData,
  creators,
  emailStatusMsg,
  sendingId,
  handleSendEmail,
  fetchDbData,
  isLoading
}) {
  const getOutreachStats = () => {
    const total = outreachData.length;
    const sent = outreachData.filter(d => d.email_status === "sent").length;
    const pending = outreachData.filter(d => d.email_status === "pending").length;
    const failed = outreachData.filter(d => d.email_status === "failed").length;
    return { total, sent, pending, failed };
  };

  const stats = getOutreachStats();

  const getBadgeClass = (status) => {
    const s = status || 'pending';
    const base = "inline-block px-2.5 py-1 rounded text-[11px] font-bold uppercase tracking-wider ";
    if (s === 'pending') return base + "bg-accent-warning/15 text-accent-warning";
    if (s === 'sending') return base + "bg-accent-secondary/15 text-accent-secondary animate-pulse";
    if (s === 'sent') return base + "bg-accent-primary/15 text-accent-primary";
    if (s === 'failed') return base + "bg-accent-danger/15 text-accent-danger";
    return base + "bg-gray-500/15 text-gray-400";
  };

  return (
    <div className="flex flex-col gap-6">
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-bg-secondary border border-border-glass rounded-lg p-5 flex flex-col">
          <span className="text-xs uppercase text-text-secondary tracking-wider">Total Drafts</span>
          <span className="text-3xl font-bold mt-1 text-white">{stats.total}</span>
        </div>
        <div className="bg-bg-secondary border border-border-glass rounded-lg p-5 flex flex-col border-l-[3px] border-accent-warning">
          <span className="text-xs uppercase text-text-secondary tracking-wider">Pending</span>
          <span className="text-3xl font-bold mt-1 text-accent-warning">{stats.pending}</span>
        </div>
        <div className="bg-bg-secondary border border-border-glass rounded-lg p-5 flex flex-col border-l-[3px] border-accent-primary">
          <span className="text-xs uppercase text-text-secondary tracking-wider">Sent</span>
          <span className="text-3xl font-bold mt-1 text-accent-primary">{stats.sent}</span>
        </div>
        <div className="bg-bg-secondary border border-border-glass rounded-lg p-5 flex flex-col border-l-[3px] border-accent-danger">
          <span className="text-xs uppercase text-text-secondary tracking-wider">Failed</span>
          <span className="text-3xl font-bold mt-1 text-accent-danger">{stats.failed}</span>
        </div>
      </div>

      <div className="bg-bg-glass backdrop-blur-md border border-border-glass rounded-xl shadow-main p-6 transition-all duration-200 hover:border-white/12">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
          <h3 className="text-lg font-semibold text-white">Outreach Delivery Hub</h3>
          <button
            className="bg-bg-tertiary border border-border-glass text-white px-4 py-2 rounded-md font-medium cursor-pointer flex items-center gap-2 transition-all duration-200 hover:bg-white/5 hover:border-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            onClick={fetchDbData}
            disabled={isLoading}
          >
            Refresh Statuses
          </button>
        </div>

        {emailStatusMsg && (
          <div
            className={`p-3 rounded-md text-sm my-3 border ${
              emailStatusMsg.includes("Error")
                ? "bg-accent-danger/10 border-accent-danger/25 text-accent-danger"
                : "bg-accent-primary/10 border-accent-primary/25 text-accent-primary"
            }`}
          >
            {emailStatusMsg}
          </div>
        )}

        <div className="overflow-x-auto mt-4 rounded-lg border border-border-glass">
          <table className="w-full border-collapse text-left text-sm">
            <thead>
              <tr className="border-b border-border-glass">
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Creator ID</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Handle/Username</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email Address</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email Subject</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email Status</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Instagram DM Status</th>
                <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Outbound Actions</th>
              </tr>
            </thead>
            <tbody>
              {outreachData.map((o) => {
                const c = creators.find(cr => cr.id === o.creator_id);
                const username = c ? c.username : `ID: ${o.creator_id}`;
                const email = c ? c.contact_email : "Unknown";

                return (
                  <tr key={o.creator_id} className="border-b border-border-glass hover:bg-white/1">
                    <td className="px-4 py-4 font-mono text-xs text-text-muted">{o.creator_id}</td>
                    <td className="px-4 py-4 font-semibold text-text-main">@{username}</td>
                    <td className={`px-4 py-4 font-medium ${email === "Not Found" ? "text-text-muted" : "text-accent-primary"}`}>{email}</td>
                    <td className="px-4 py-4 text-xs text-text-secondary">{o.email_subject}</td>
                    <td className="px-4 py-4">
                      <span className={getBadgeClass(o.email_status)}>
                        {o.email_status || 'pending'}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      <span className={getBadgeClass(o.instagram_dm_status)}>
                        {o.instagram_dm_status || 'pending'}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      <button
                        className="bg-accent-primary text-black font-bold border-none px-3.5 py-1.5 rounded cursor-pointer transition-all duration-200 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-xs flex items-center gap-1.5"
                        disabled={email === "Not Found" || o.email_status === "sent" || sendingId === o.creator_id}
                        onClick={() => handleSendEmail(o.creator_id)}
                      >
                        {sendingId === o.creator_id ? "Sending..." : "✉️ Send Email"}
                      </button>
                    </td>
                  </tr>
                );
              })}
              {outreachData.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center text-text-muted py-8 text-sm">
                    No outreach drafts exist. Run the scraper to populate creator candidates.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
