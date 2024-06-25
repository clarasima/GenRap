<script setup>
</script>

<template>
  <div>
    <main>
      <section class="intro">
        <h2>Welcome to GenRap!</h2>
        <p>
          Our application helps you automatically manage your academic
          publications and citations, providing you with the ability to quickly
          generate detailed reports.
        </p>
      </section>

      <section class="features">
        <h2>Key Features</h2>
        <ul>
          <li>Automated extraction of publications and citations</li>
          <li>Report generation in Excel, CSV, and TXT formats</li>
          <li>User-friendly and easy-to-use interface</li>
        </ul>
      </section>

      <section class="contact-support">
        <h2>Contact and Support</h2>
        <p>
          For questions or assistance, you can contact us at
          <a href="mailto:clara.sima17@gmail.com">clara.sima17@gmail.com</a>.
        </p>
      </section>
    </main>

  </div>
</template>

<style scoped>
.image-container {
  width: 300px;
  /* Set the desired width */
  height: auto;
  /* Set the desired height to crop vertically */
  overflow: hidden;
  /* Hide the overflow to crop the image */
  position: relative;
  /* Position context for the image */
}

.cropped-image {
  width: 100%;
  /* Ensures the image fills the container width */
  height: auto;
  /* Maintains the aspect ratio */
  object-fit: cover;
  /* Scale the image to cover the container */
  object-position: center;
  /* Center the image within the container */
  clip-path: inset(17% 0 17% 0);
  /* Clip 20% from top and bottom, showing the middle 60% */
}

main {
  padding: 2em;
}
.intro,
.features,
.auth-options,
.contact-support,
.testimonials {
  margin-bottom: 2em;
}
h1,
h2 {
  color: var(--primary);
}
ul {
  list-style-type: none;
  padding: 0;
}
ul li {
  background: #e0e0e0;
  margin: 0.5em 0;
  padding: 0.5em;
  border-radius: 5px;
}

a {
  color: var(--teal--500);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}

</style>
