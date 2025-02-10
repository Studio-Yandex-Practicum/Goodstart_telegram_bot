document.addEventListener("DOMContentLoaded", function () {
  const days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
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
    "декабря"
  ];
  const accordionItems = document.querySelectorAll(".accordion-item");

  // Функция для получения даты на нужной неделе
  function getDateForWeek(weekOffset, index) {
    const today = new Date();
    const startOfWeek = new Date(today.getTime() + (weekOffset * 7 * 24 * 60 * 60 * 1000));
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + index + 1); // +1 чтобы начать с текущего дня
    return startOfWeek;
  }

  // Функция для обновления дат в аккордеоне
  function updateAccordionDates(weekOffset) {
    const today = new Date();
    accordionItems.forEach((item, index) => {
      const headerButton = item.querySelector(".accordion-header .accordion-button");
      const dayName = days[index];
      const newDate = getDateForWeek(weekOffset, index);
      headerButton.innerHTML = `${dayName}, ${newDate.getDate()} ${months[newDate.getMonth()]}`;

      // Сравниваем даты, чтобы открыть текущий день
      if (today.getDate() === newDate.getDate() && today.getMonth() === newDate.getMonth()) {
        const currentDayAccordion = item.querySelector(".accordion-collapse");
        currentDayAccordion.classList.add("show");
        const currentDayButton = item.querySelector(".accordion-header .accordion-button");
        currentDayButton.setAttribute("aria-expanded", "true");
        currentDayButton.classList.remove("collapsed");
      }
    });

    // Обновляем ссылки "Предыдущая неделя" и "Следующая неделя"
    const prevWeekLink = document.querySelector(".btn-previous-week");
    const nextWeekLink = document.querySelector(".btn-next-week");
    if (prevWeekLink) {
      prevWeekLink.setAttribute("href", `?week=${weekOffset - 1}`);
    }
    if (nextWeekLink) {
      nextWeekLink.setAttribute("href", `?week=${weekOffset + 1}`);
    }
  }

  // Получаем текущее значение week_offset из параметров URL
  const urlParams = new URLSearchParams(window.location.search);
  const weekOffset = parseInt(urlParams.get('week')) || 0;

  // Инициализируем аккордеон при загрузке страницы
  updateAccordionDates(weekOffset);
});