// document.addEventListener("DOMContentLoaded", () => {
//     const listEl = document.getElementById("list");
//     const form = document.getElementById("post-form");
//     const titleEl = document.getElementById("title");
//     const contentEl = document.getElementById("content");
  
//     const load = async () => {
//       const res = await fetch("/api/posts");
//       const data = await res.json();
//       listEl.innerHTML = data.map(p => `<li><b>${escapeHtml(p.title)}</b> - ${escapeHtml(p.content)}</li>`).join("");
//     };
  
//     form.addEventListener("submit", async (e) => {
//       e.preventDefault();
//       await fetch("/api/posts", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ title: titleEl.value, content: contentEl.value })
//       });
//       titleEl.value = "";
//       contentEl.value = "";
//       await load();
//     });
  
//     const escapeHtml = (s="") => s.replace(/[&<>"']/g, c => ({
//       "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
//     }[c]));
  
//     load();
//   });