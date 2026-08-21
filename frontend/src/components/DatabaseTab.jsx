import React from "react";

export default function DatabaseTab({
  activeDbTab,
  setActiveDbTab,
  creators,
  reels,
  outreachData,
  isLoading,
  errorMsg,
  fetchDbData
}) {
  return (
    <div className="bg-bg-glass backdrop-blur-md border border-border-glass rounded-xl shadow-main p-6 transition-all duration-200 hover:border-white/12">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Database Explorer</h3>
          <p className="text-xs text-text-secondary mt-1">
            Inspect live rows currently stored in Supabase tables
          </p>
        </div>
        <button
          className="bg-bg-tertiary border border-border-glass text-white px-4 py-2 rounded-md font-medium cursor-pointer flex items-center gap-2 transition-all duration-200 hover:bg-white/5 hover:border-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
          onClick={fetchDbData}
          disabled={isLoading}
        >
          Refresh Tables
        </button>
      </div>

      {errorMsg && (
        <p className="text-accent-danger text-sm my-2">{errorMsg}</p>
      )}

      <div className="flex gap-2 border-b border-border-glass pb-2 mb-4 overflow-x-auto">
        <button
          className={`px-4 py-2 text-sm cursor-pointer rounded transition-all duration-200 shrink-0 border-none ${
            activeDbTab === "creators"
              ? "bg-white/5 text-accent-secondary font-medium"
              : "bg-transparent text-text-secondary hover:text-white"
          }`}
          onClick={() => setActiveDbTab("creators")}
        >
          Creators ({creators.length})
        </button>
        <button
          className={`px-4 py-2 text-sm cursor-pointer rounded transition-all duration-200 shrink-0 border-none ${
            activeDbTab === "reels"
              ? "bg-white/5 text-accent-secondary font-medium"
              : "bg-transparent text-text-secondary hover:text-white"
          }`}
          onClick={() => setActiveDbTab("reels")}
        >
          Reels ({reels.length})
        </button>
        <button
          className={`px-4 py-2 text-sm cursor-pointer rounded transition-all duration-200 shrink-0 border-none ${
            activeDbTab === "outreach"
              ? "bg-white/5 text-accent-secondary font-medium"
              : "bg-transparent text-text-secondary hover:text-white"
          }`}
          onClick={() => setActiveDbTab("outreach")}
        >
          Outreach Drafts ({outreachData.length})
        </button>
      </div>

      {isLoading ? (
        <div className="py-8 text-center text-text-secondary font-mono text-sm">
          Querying Supabase database proxy...
        </div>
      ) : (
        <div className="overflow-x-auto mt-4 rounded-lg border border-border-glass">
          {activeDbTab === "creators" && (
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-border-glass">
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">ID</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Username</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Name</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Followers</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Engagement</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Niche Category</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email</th>
                </tr>
              </thead>
              <tbody>
                {creators.map((c) => (
                  <tr key={c.id} className="border-b border-border-glass hover:bg-white/1">
                    <td className="px-4 py-4 font-mono text-xs text-text-muted">{c.id}</td>
                    <td className="px-4 py-4 font-semibold text-accent-secondary">
                      <a href={c.profile_url} target="_blank" rel="noreferrer" className="hover:underline">
                        @{c.username}
                      </a>
                    </td>
                    <td className="px-4 py-4 text-text-main font-medium">{c.name}</td>
                    <td className="px-4 py-4 text-text-main">{c.follower_count ? c.follower_count.toLocaleString() : "N/A"}</td>
                    <td className="px-4 py-4 text-text-main">{c.engagement_rate ? `${c.engagement_rate}%` : "N/A"}</td>
                    <td className="px-4 py-4 text-text-main">
                      <span className="text-xs bg-white/3 px-2 py-1 rounded">
                        {c.category}
                      </span>
                    </td>
                    <td className={`px-4 py-4 font-medium ${c.contact_email === "Not Found" ? "text-text-muted" : "text-accent-primary"}`}>
                      {c.contact_email}
                    </td>
                  </tr>
                ))}
                {creators.length === 0 && (
                  <tr>
                    <td colSpan="7" className="text-center text-text-muted py-8 text-sm">
                      No creators in database yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}

          {activeDbTab === "reels" && (
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-border-glass">
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">ID</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Creator ID</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Reel URL</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Likes</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Comments</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Caption/Description Snippet</th>
                </tr>
              </thead>
              <tbody>
                {reels.map((r) => (
                  <tr key={r.id} className="border-b border-border-glass hover:bg-white/1">
                    <td className="px-4 py-4 font-mono text-xs text-text-muted">{r.id}</td>
                    <td className="px-4 py-4 font-mono text-xs text-text-main">{r.creator_id}</td>
                    <td className="px-4 py-4 text-text-main">
                      <a href={r.instagram_url} target="_blank" rel="noreferrer" className="text-accent-secondary hover:underline">
                        View Reel 
                      </a>
                    </td>
                    <td className="px-4 py-4 text-text-main">{r.likes ? r.likes.toLocaleString() : 0}</td>
                    <td className="px-4 py-4 text-text-main">{r.comments ? r.comments.toLocaleString() : 0}</td>
                    <td className="px-4 py-4 max-w-[300px] overflow-hidden text-ellipsis whitespace-nowrap text-xs text-text-secondary">
                      {r.description || "No description"}
                    </td>
                  </tr>
                ))}
                {reels.length === 0 && (
                  <tr>
                    <td colSpan="6" className="text-center text-text-muted py-8 text-sm">
                      No reels in database yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}

          {activeDbTab === "outreach" && (
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-border-glass">
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Creator ID</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email Subject</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Email Body Preview</th>
                  <th className="bg-bg-secondary text-text-secondary font-medium px-4 py-3 text-xs uppercase tracking-wider">Instagram DM Draft</th>
                </tr>
              </thead>
              <tbody>
                {outreachData.map((o) => (
                  <tr key={o.creator_id} className="border-b border-border-glass hover:bg-white/1">
                    <td className="px-4 py-4 font-mono text-xs text-text-main">{o.creator_id}</td>
                    <td className="px-4 py-4 text-text-main font-medium">{o.email_subject}</td>
                    <td className="px-4 py-4 max-w-[250px] overflow-hidden text-ellipsis whitespace-nowrap text-xs text-text-secondary">
                      {o.email_body}
                    </td>
                    <td className="px-4 py-4 max-w-[250px] overflow-hidden text-ellipsis whitespace-nowrap text-xs text-text-secondary">
                      {o.instagram_dm}
                    </td>
                  </tr>
                ))}
                {outreachData.length === 0 && (
                  <tr>
                    <td colSpan="4" className="text-center text-text-muted py-8 text-sm">
                      No outreach drafts generated yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
