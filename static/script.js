document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const input = document.getElementById("pergunta");

    form.addEventListener("submit", function () {
        setTimeout(() => {
            input.value = "";
        }, 100); // Pequeno delay para garantir que o form envie os dados
    });
});