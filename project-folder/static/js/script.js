const form = document.getElementById('analysisForm');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const loadingText = document.getElementById('loadingText');
const resultsContainer = document.getElementById('resultsContainer');
const resultsDiv = document.getElementById('results');

form.addEventListener('submit', async (event) => {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the form data
    const fund = document.getElementById('fund').value;
    const depth = document.getElementById('depth').value;
    const investment = document.getElementById('investment').value;
    const units = document.getElementById('units').value;

    // Show the progress bar
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    loadingText.textContent = 'Starting analysis...';
    resultsContainer.style.display = 'none';

    // Prepare form data
    const formData = new FormData();
    formData.append('fund', fund);
    formData.append('depth', depth);
    formData.append('investment', investment);
    formData.append('units', units);

    // Start progress bar animation
    let delay = 100;
    if (fund == "latest_nav_hdfcflexicap") { delay = depth === '1' ? 15000 : 110000; }
    else if (fund == "latest_nav_jmflexicap") { delay = depth === '1' ? 15000 : 130000; }
    else if (fund == "latest_nav_motilallargeandmidcap") { delay = depth === '1' ? 15000 : 65000; }
    else if (fund == "latest_nav_motilalsmallcap") { delay = depth === '1' ? 15000 : 90000; }
    else if (fund == "latest_nav_trustsmallcap") { delay = depth === '1' ? 15000 : 110000; }
    else if (fund == "latest_nav_bandhansmallcap") { delay = depth === '1' ? 15000 : 350000 }
    const totalTime = delay;
    const totalSteps = 100;
    const interval = totalTime / totalSteps;

    let currentProgress = 0;

    const progressInterval = setInterval(() => {
        currentProgress += 1;

        if (currentProgress <= 10) {
            progressBar.style.width = `${currentProgress}%`;
            loadingText.textContent = `Fetching Fund's Previous NAV... ${currentProgress}%`;
        } else if (currentProgress <= 25) {
            progressBar.style.width = `${currentProgress}%`;
            loadingText.textContent = `Analyzing Fund's current holding distribution... ${currentProgress}%`;
        } else if (currentProgress <= 50) {
            progressBar.style.width = `${currentProgress}%`;
            loadingText.textContent = `Getting yesterday's closing prices of individual stocks... ${currentProgress}%`;
        } else if (currentProgress <= 75) {
            progressBar.style.width = `${currentProgress}%`;
            loadingText.textContent = `Finding current prices of individual stocks... ${currentProgress}%`;
        } else if (currentProgress < 100) {
            progressBar.style.width = `${currentProgress}%`;
            loadingText.textContent = `Calculating New NAV... ${currentProgress}%`;
        } else if (currentProgress >= 100) {
            clearInterval(progressInterval);
            progressBar.style.width = `${100}%`;
            loadingText.textContent = 'Analysis complete! Loading results...';
        }
    }, interval);

    // Send the request to the backend and wait for response
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });

        const html = await response.text(); // Get HTML content of results
        clearInterval(progressInterval); // Ensure progress stops
        loadingText.textContent = '';
        progressContainer.style.display = 'none';

        // Display the results in the results container
        resultsDiv.innerHTML = html;
        resultsContainer.style.display = 'block';

    } catch (error) {
        clearInterval(progressInterval); // Stop progress on error
        loadingText.textContent = 'Error: Unable to complete analysis. Restart app.py and then refresh the page.';
        console.error(error);
    }
});
