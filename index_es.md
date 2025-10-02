---
title: Desarrollar Agentes de IA en Azure
permalink: index.html
layout: home
---

Los siguientes ejercicios están diseñados para proporcionarte una experiencia de aprendizaje práctica en la que explorarás tareas comunes que los desarrolladores realizan al construir agentes de IA en Microsoft Azure.

> **Nota**: Para completar los ejercicios, necesitarás una suscripción de Azure en la que tengas permisos y cuota suficientes para aprovisionar los recursos de Azure necesarios y modelos de IA generativa. Si aún no tienes una, puedes registrarte para obtener una [cuenta de Azure](https://azure.microsoft.com/free). Hay una opción de prueba gratuita para nuevos usuarios que incluye créditos para los primeros 30 días.

## Ejercicios

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
<hr>
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

{% endfor %}

<hr>

> **Nota**: Si bien puedes completar estos ejercicios por tu cuenta, están diseñados para complementar módulos en [Microsoft Learn](https://learn.microsoft.com/training/paths/develop-ai-agents-on-azure/); donde encontrarás una inmersión más profunda en algunos de los conceptos subyacentes en los que se basan estos ejercicios.

