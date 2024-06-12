// Когда весь HTML-документ загружен...
document.addEventListener("DOMContentLoaded", function () {
  const days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
  ];
  const months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
  ];
  const accordionItems = document.querySelectorAll(".accordion-item");
  const today = new Date();
  // Вычисляем индекс текущего дня недели (Понедельник = 0, Вторник = 1, ..., Суббота = 5)
  let dayIndex = today.getDay() - 1;

  // Если сегодня воскресенье (dayIndex < 0), устанавливаем индекс дня на понедельник следующей недели
  if (dayIndex < 0) {
    dayIndex = 0;
    today.setDate(today.getDate() + 1);
  }

  const date = today.getDate();

  // Устанавливаем номера для каждого дня в аккордеоне
  accordionItems.forEach((item, index) => {
    const headerButton = item.querySelector(
      ".accordion-header .accordion-button"
    );
    const dayName = days[index];
    const newDate = new Date(
      today.getFullYear(),
      today.getMonth(),
      date - dayIndex + index
    );
    headerButton.innerHTML = `${dayName}, ${newDate.getDate()} ${months[newDate.getMonth()]
      }`;
  });

  // Открываем текущий день в аккордеоне
  if (dayIndex >= 0 && dayIndex < accordionItems.length) {
    const currentDayAccordion = accordionItems[dayIndex].querySelector(
      ".accordion-collapse"
    );
    currentDayAccordion.classList.add("show");
    const currentDayButton = accordionItems[dayIndex].querySelector(
      ".accordion-header .accordion-button"
    );
    currentDayButton.setAttribute("aria-expanded", "true");
    currentDayButton.classList.remove("collapsed");
  }
});