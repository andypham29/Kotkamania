const nullish = (v) =>
    (v === null || v === undefined || v === "" || v === "null")
        ? `<span class="fp-nullish">—</span>`
        : v;

const timeFromSeconds = (v) =>
  (v === null || v === undefined || v === "" || isNaN(v))
    ? `<span class="fp-nullish">—</span>`
    : (() => {
        const total = Number(v);

        // Round UP to the next whole second
        const rounded = Math.ceil(total);

        const hours = Math.floor(rounded / 3600);
        const minutes = Math.floor((rounded % 3600) / 60);
        const seconds = rounded % 60;

        return hours > 0
          ? `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`
          : `${minutes}:${String(seconds).padStart(2, "0")}`;
      })();


