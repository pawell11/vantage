const MODAL_DELAY_MS = 18000;
const MODAL_DISMISS_KEY = "vantage_modal_dismissed";

window.scrollTo(0, 0);

const tabs = document.querySelectorAll(".ptab");
const panels = document.querySelectorAll(".ppanel");
const revealSections = document.querySelectorAll(".reveal");
const callModal = document.getElementById("callModal");
const callModalClose = document.getElementById("callModalClose");
const copyEmailBtn = document.getElementById("copyEmailBtn");

let hasShownCallModal = false;
let modalTimer = null;

function setActiveTab(tabName) {
  tabs.forEach((tab) => {
    const isActive = tab.dataset.tab === tabName;
    tab.classList.toggle("is-active", isActive);
    tab.setAttribute("aria-selected", String(isActive));
  });
  panels.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.panel === tabName);
  });
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => setActiveTab(tab.dataset.tab));
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

revealSections.forEach((section) => observer.observe(section));

function isDismissed() {
  try {
    return sessionStorage.getItem(MODAL_DISMISS_KEY) === "1";
  } catch {
    return false;
  }
}

function rememberDismissed() {
  try {
    sessionStorage.setItem(MODAL_DISMISS_KEY, "1");
  } catch {
    /* ignore */
  }
}

function openModal() {
  if (!callModal || hasShownCallModal) return;
  callModal.classList.add("is-visible");
  callModal.setAttribute("aria-hidden", "false");
  hasShownCallModal = true;
  if (modalTimer) {
    clearTimeout(modalTimer);
    modalTimer = null;
  }
}

function closeModal() {
  if (!callModal) return;
  callModal.classList.remove("is-visible");
  callModal.setAttribute("aria-hidden", "true");
  rememberDismissed();
}

function toggleBottomPopup() {
  if (!callModal || hasShownCallModal || isDismissed()) return;
  if (window.scrollY < 200) return;
  const triggerOffset = 220;
  const nearBottom =
    window.scrollY + window.innerHeight >=
    document.documentElement.scrollHeight - triggerOffset;
  if (nearBottom) openModal();
}

if (!isDismissed()) {
  modalTimer = setTimeout(() => {
    if (!hasShownCallModal) openModal();
  }, MODAL_DELAY_MS);
}

window.addEventListener("scroll", toggleBottomPopup, { passive: true });
window.addEventListener("resize", toggleBottomPopup);

if (callModalClose) callModalClose.addEventListener("click", closeModal);

if (callModal) {
  callModal.addEventListener("click", (event) => {
    if (event.target === callModal) closeModal();
  });
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && callModal && callModal.classList.contains("is-visible")) {
    closeModal();
  }
});

function showToast(text) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = text;
  requestAnimationFrame(() => toast.classList.add("is-visible"));
  setTimeout(() => toast.classList.remove("is-visible"), 1800);
}

if (copyEmailBtn) {
  copyEmailBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      await navigator.clipboard.writeText("vantageaiservices@gmail.com");
      showToast("Email copied to clipboard");
    } catch {
      window.location.href = "mailto:vantageaiservices@gmail.com";
    }
  });
}
