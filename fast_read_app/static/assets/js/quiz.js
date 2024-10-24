$('document').ready(function() {
    

    let allowTurning = false;
    
    const $mobileMenulinks = $('.mobile-menu-link');
    function turn_page(selected = false,questionId = 0){
        if (selected == false){
            allowTurning = true;
            $('#magazine').turn('next');
        }
        else {
            let selectedAnswer = $(`input[name=f{selected}]:checked`).val();
            if (selectedAnswer !== undefined) {
                userAnswers[questionId] = [parseInt(selectedAnswer)];
                allowTurning = true;
                $('#magazine').turn('next');
            }
            else {
                alert('Жауапты таңдаңыз.');
                return;
            }
            
        } 
          
    }

    $mobileMenulinks.on('click', function (e) {
        $('body').removeClass('canvas_expanded');
    });
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
        return csrfToken;
    }

    async function fetchTestData() {
        try {
            const response = await fetch('/get_text_and_questions/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            });
            if (!response.ok) {
                throw new Error('Failed to fetch test data.');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching test data:', error);
            alert('Тест деректерін жүктеу кезінде қате орын алды.');
        }
    }

    let timerInterval;
    let secondsElapsed = 0;
    let testData = {};
    let currentQuestionIndex = 0;
    let userAnswers = {};
    
    $(document).ready(function () {
        fetchTestData().then(data => {
            if (data) {
                testData = data;
                $('#story-text').text(data.text);
            }
        }).then(()=>{
             testData.questions.forEach(element => {
                showQuestion()
                currentQuestionIndex ++
            });
        }).then(()=>{
            $("#magazine").append(
            `
            <div style="background-color: white;">
                        <div id="question-container">
                                <!-- WhatsApp Number Input -->
                                <div id="whatsapp-input">
                                    <div class="mb-3">
                                        <label for="whatsapp_number" class="form-label">WhatsApp номеріңіз:</label>
                                        <input type="text" id="whatsapp_number" name="whatsapp_number" required>
                                    </div>
                                    <div class="text-center">
                                        <button type="submit" id="submit-btn">Жіберу</button>
                                    </div>
                                </div>
                        </div>
                    </div>
            `
            )
        }).then(()=>{
            $('#magazine').turn({
                
                display: 'single',
                acceleration: true,
                gradients: !$.isTouch,
                elevation:50,
                when: {
                    turning: function(event, page, view) {
                            if (!allowTurning) {
                                event.preventDefault(); 
                            }
                    },
                    turned: function(e, page) {
                        allowTurning = false;
                    }
                }
            });
        });

        $('.start-btn').click(function () {
            $(this).fadeOut();
            $('#text-container').fadeIn();
            $('#ready-btn').fadeIn();
            $('#progress-bar').fadeIn();
            startTimer();
            turn_page();
            $('.tj-footer-three')[0].scrollIntoView({
                behavior: 'smooth'  // Плавная прокрутка
            });
        });

        $('#ready-btn').click(function () {
            stopTimer();
            $('#text-container').fadeOut();
            $('#ready-btn').fadeOut();
            $('#progress-bar').fadeOut();
            turn_page();
        });



        $('#quiz-form').submit(function (event) {
            event.preventDefault();

            let whatsappNumber = $('#whatsapp_number').val();
            if (!whatsappNumber) {
                alert('WhatsApp номеріңізді енгізіңіз.');
                return;
            }

            let payload = {
                id: testData.id,
                text: testData.text,
                whatsapp_number: whatsappNumber,
                time: secondsElapsed,
                answers: userAnswers
            };

            const csrfToken = getCSRFToken();

            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(payload),
                credentials: 'same-origin'
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Жауапты жіберу кезінде қате орын алды.');
                    }
                    return response.json();
                })
                .then(responseData => {
                    $('#whatsapp-input').html(`
                        <div class="container text-center" style="padding: 100px 0;">
                            <h2 class="mt-5">Рахмет!</h2>
                            <p>Сіздің жауабыңыз қабылданды!</p>
                        </div>
                    `);
                    console.log(responseData);
                })
                .catch(error => {
                    console.error('Қате:', error);
                });
        });
    });

    function startTimer() {
        timerInterval = setInterval(() => {
            secondsElapsed++;
            $('#timer').text(`Уақыт: ${secondsElapsed} секунд`);
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    function showQuestion() {
        $('#question-container').fadeIn();
        let questionData = testData.questions[currentQuestionIndex];
        
        if (questionData) {
            let questionHtml = `
                    <div style="background-color: white;">
                        <div id="question-container">
                            <h2 class="mb-4 text-center">Тест</h2>                                
                                <div id="question-content">
                                    <div class="question mb-4">
                                    <h5>${currentQuestionIndex + 1}. ${questionData.question}</h5>`;
            questionData.answers.forEach(a => {
                questionHtml += `<div class="form-check">
                                    <input class="form-check-input" type="radio" name="question_option_${currentQuestionIndex}" id="option_${a.id}" value="${a.id}" >
                                    <label class="form-check-label" for="option_${a.id}">
                                        ${a.answer}
                                    </label>
                                 </div>`;
            });
            questionHtml += `</div></div>

                                <!-- Кнопка "Келесі" внутри блока теста -->
                                <div id="next-button" onclick="turn_page(selected = 'question_option_${currentQuestionIndex}', ${questionData.id})" class="text-center">
                                    <span class="next-btn">Келесі</span>
                                </div>

                        
                        </div>`;
            $('#magazine').append(questionHtml)

            $('#next-button').show();
        }
    }
});
