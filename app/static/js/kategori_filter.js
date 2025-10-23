console.log("kategori_filter.js yüklendi ✅");
document.addEventListener("DOMContentLoaded", () => {
  const kategoriButtons = document.querySelectorAll(".kategori-btn");
  const etkinliklerContainer = document.getElementById("etkinlikler-container");

  kategoriButtons.forEach(btn => {
    btn.addEventListener("click", async () => {
      const kategoriId = btn.dataset.id;

      // Eğer 0'a basıldıysa (Tüm Etkinlikler)
      if (kategoriId === "0") {
        const response = await fetch("/etkinlikler");
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        const newContent = doc.querySelector("#etkinlikler-container").innerHTML;
        etkinliklerContainer.innerHTML = newContent;
        return;
      }

      // Diğer kategoriler için
      const response = await fetch(`/kategori/${kategoriId}`);
      const data = await response.json();

      // Eski içeriği temizle
      etkinliklerContainer.innerHTML = "";

      if (data.length === 0) {
        etkinliklerContainer.innerHTML = "<p>Bu kategoride etkinlik bulunamadı.</p>";
        return;
      }

      // Yeni kartları oluştur
            data.forEach(etkinlik => {
        const link = document.createElement("a");
        link.href = `/etkinlik_detay/${etkinlik[2]}`; // etkinlikID burada 3. sütun
        link.classList.add("card-link");

        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
          <img class="card-img-top" src="/static/${etkinlik[1]}" alt="${etkinlik[0]}">
          <div class="card-overlay">
            <h5 class="card-title">${etkinlik[0]}</h5>
          </div>`;

        link.appendChild(card);
        etkinliklerContainer.appendChild(link);
      });
    });
  });
});
