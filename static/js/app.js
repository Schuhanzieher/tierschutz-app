document.addEventListener("DOMContentLoaded", function () {
    var searchInput = document.getElementById("search-input");
    var contactCount = document.getElementById("contact-count");
    var rows = document.querySelectorAll("#contact-table tbody tr");

    // Client-Side Textsuche (sofort, ohne Seitenreload)
    if (searchInput && rows.length > 0) {
        searchInput.addEventListener("input", function () {
            var query = this.value.toLowerCase();
            var visible = 0;

            rows.forEach(function (row) {
                var text = row.textContent.toLowerCase();
                if (!query || text.indexOf(query) !== -1) {
                    row.style.display = "";
                    visible++;
                } else {
                    row.style.display = "none";
                }
            });

            if (contactCount) {
                contactCount.textContent = visible;
            }
        });
    }

    // Heutiges Datum als Default fuer Aktivitaets-Formular
    var dateInputs = document.querySelectorAll('input[type="date"][name="datum"]');
    dateInputs.forEach(function (input) {
        if (!input.value) {
            var today = new Date().toISOString().split("T")[0];
            input.value = today;
        }
    });

    // ── Chat: Username-System ─────────────────────────────────
    var globalUsername = document.getElementById("global-username");
    var sidebarAvatar = document.getElementById("sidebar-avatar");
    var chatAbsenderHidden = document.getElementById("chat-absender-hidden");
    var rubrikBenutzername = document.getElementById("rubrik-benutzername");

    function updateChatUsername() {
        var name = globalUsername ? globalUsername.value.trim() : "";
        if (name) {
            localStorage.setItem("chat-username", name);
            if (sidebarAvatar) sidebarAvatar.textContent = name[0].toUpperCase();
            if (chatAbsenderHidden) chatAbsenderHidden.value = name;
            if (rubrikBenutzername) rubrikBenutzername.value = name;
        } else {
            if (sidebarAvatar) sidebarAvatar.textContent = "?";
        }
    }

    if (globalUsername) {
        var savedName = localStorage.getItem("chat-username");
        if (savedName) {
            globalUsername.value = savedName;
        }
        updateChatUsername();
        globalUsername.addEventListener("input", updateChatUsername);
        globalUsername.addEventListener("change", updateChatUsername);
    }

    // ── Chat: Auto-Scroll + Polling ─────────────────────────────
    var chatBox = document.getElementById("chat-box");
    if (chatBox) {
        // Ans Ende scrollen
        chatBox.scrollTop = chatBox.scrollHeight;

        var rubrikId = chatBox.getAttribute("data-rubrik-id") || 0;

        // Letzte bekannte ID ermitteln
        var lastId = 0;
        var allMsgs = chatBox.querySelectorAll(".chat-bubble");
        if (allMsgs.length > 0) {
            lastId = parseInt(allMsgs[allMsgs.length - 1].getAttribute("data-id")) || 0;
        }

        // Farbe fuer einen Namen berechnen
        function nameToColor(name) {
            var hash = 0;
            for (var i = 0; i < name.length; i++) {
                hash = name.charCodeAt(i) + ((hash << 5) - hash);
            }
            var hue = Math.abs(hash % 360);
            return "hsl(" + hue + ", 60%, 45%)";
        }

        // Polling alle 3 Sekunden
        setInterval(function () {
            fetch("/chat/api?after=" + lastId + "&rubrik_id=" + rubrikId)
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.messages && data.messages.length > 0) {
                        // Leeren Hinweis entfernen
                        var empty = document.getElementById("chat-empty");
                        if (empty) empty.remove();

                        data.messages.forEach(function (m) {
                            var div = document.createElement("div");
                            div.className = "chat-bubble";
                            div.setAttribute("data-id", m.id);
                            var initial = m.absender ? m.absender[0].toUpperCase() : "?";
                            var color = nameToColor(m.absender || "");
                            div.innerHTML =
                                '<div class="chat-bubble-avatar" style="background-color: ' + color + '">' +
                                    escapeHtml(initial) +
                                '</div>' +
                                '<div class="chat-bubble-content">' +
                                    '<div class="chat-bubble-header">' +
                                        '<strong class="chat-bubble-name">' + escapeHtml(m.absender) + '</strong>' +
                                        '<span class="chat-bubble-time">' + escapeHtml(m.zeit) + '</span>' +
                                    '</div>' +
                                    '<div class="chat-bubble-text">' + escapeHtml(m.nachricht) + '</div>' +
                                '</div>';
                            chatBox.appendChild(div);
                            lastId = m.id;
                        });
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                })
                .catch(function () {});
        }, 3000);

        // Form-Submit: Username pruefen
        var chatForm = document.getElementById("chat-form");
        var chatSendBtn = document.getElementById("chat-send-btn");
        if (chatForm) {
            chatForm.addEventListener("submit", function (e) {
                var name = globalUsername ? globalUsername.value.trim() : "";
                if (!name) {
                    e.preventDefault();
                    globalUsername.focus();
                    globalUsername.style.borderColor = "#ef4444";
                    globalUsername.setAttribute("placeholder", "Bitte Name eingeben!");
                    setTimeout(function () {
                        globalUsername.style.borderColor = "";
                        globalUsername.setAttribute("placeholder", "Dein Name...");
                    }, 2000);
                    return false;
                }
                if (chatAbsenderHidden) chatAbsenderHidden.value = name;
            });
        }
    }

    // ── Text-Generator: Kontakt uebernehmen ────────────────────
    var kontaktSelect = document.getElementById("kontakt-select");
    if (kontaktSelect) {
        kontaktSelect.addEventListener("change", function () {
            var opt = this.options[this.selectedIndex];
            if (opt.value) {
                var nameInput = document.getElementById("name");
                var orgInput = document.getElementById("organisation");
                if (nameInput) nameInput.value = opt.getAttribute("data-name") || "";
                if (orgInput) orgInput.value = opt.getAttribute("data-organisation") || "";
            }
        });
    }

    // ── Text-Generator: Felder je nach Vorlage ein-/ausblenden ─
    var vorlageSelect = document.getElementById("vorlage");
    if (vorlageSelect) {
        function updateExtraFields() {
            var val = vorlageSelect.value;
            // Alle Extra-Felder ausblenden
            document.querySelectorAll("#extra-fields > div").forEach(function (el) {
                el.style.display = "none";
            });
            // Je nach Vorlage bestimmte Felder zeigen
            if (val === "pressetext") {
                document.querySelectorAll(".field-email, .field-ort, .field-datum").forEach(function (el) {
                    el.style.display = "";
                });
            }
            if (val === "social_post") {
                document.querySelectorAll(".field-hashtags").forEach(function (el) {
                    el.style.display = "";
                });
            }
        }
        vorlageSelect.addEventListener("change", updateExtraFields);
        updateExtraFields(); // Initial ausfuehren
    }
});

// HTML-Escape fuer Chat-Nachrichten
function escapeHtml(text) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

// Text kopieren (Text-Generator)
function copyText() {
    var textEl = document.getElementById("generated-text");
    if (textEl) {
        navigator.clipboard.writeText(textEl.textContent).then(function () {
            var btn = document.getElementById("copy-btn");
            if (btn) {
                btn.textContent = "Kopiert!";
                setTimeout(function () { btn.innerHTML = "&#x1f4cb; Kopieren"; }, 2000);
            }
        });
    }
}

// Server-Side Filter (Kategorie, Status, Sortierung -> URL-Parameter)
function applyServerFilter() {
    var kat = document.getElementById("filter-kategorie");
    var status = document.getElementById("filter-status");
    var sort = document.getElementById("sort-select");

    var params = new URLSearchParams();

    if (kat && kat.value) {
        params.set("kategorie", kat.value);
    }
    if (status && status.value) {
        params.set("status", status.value);
    }
    if (sort && sort.value && sort.value !== "name") {
        params.set("sort", sort.value);
    }

    var url = window.location.pathname;
    var qs = params.toString();
    if (qs) {
        url += "?" + qs;
    }
    window.location.href = url;
}
