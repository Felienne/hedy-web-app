import {modal} from ".././modal";
import {pushAchievement, runit, theGlobalEditor} from ".././app";

let current_step = 0;
let student = true;

// We call this function on load -> customize click event of the tutorial button
(function() {
  $('#tutorial_next_button').off('click').on('click', () => {
    $('#tutorial-pop-up').hide();
    // If we are a student -> call the next student tutorial step, otherwise call the teacher step
    current_step += 1;
    if (student) {
      return callNextStep();
    }
    return callTeacherNextStep();
  });
})();

function codeEditorStep() {
  $('#editor').addClass("z-40");
  addHighlightBorder("editor");

  relocatePopup(65, 30);
  theGlobalEditor?.setValue("print ___");
  tutorialPopup(current_step);
}

function codeOutputStep() {
  removeBorder("editor");
  $('#code_output').addClass("z-40");
  addHighlightBorder("code_output");

  runit ("1", "en", "", function () {
    $ ('#output').focus ();
  });

  relocatePopup(35, 30);
  tutorialPopup(current_step);
}

function runButtonStep() {
  removeBorder("code_output");
  $('#code_related_buttons').show();
  $('#runButtonContainer').addClass("z-40");
  addHighlightBorder("runButtonContainer");

  relocatePopup(50, 30);
  tutorialPopup(current_step);
}

function tryRunButtonStep() {
  $.ajax({
      type: 'GET',
      url: '/get_tutorial_step/intro/code_snippet/',
      dataType: 'json'
    }).done(function(response: any) {
       theGlobalEditor?.setValue(response.code);
    }).fail(function() {
       theGlobalEditor?.setValue("print Hello world!\nprint I'm learning Hedy with the tutorial!");
    });

  relocatePopup(50, 70);
  tutorialPopup(current_step);
}

function speakAloudStep() {
  removeBorder("runButtonContainer");
  $('#editor').removeClass('z-40');
  $('#code_output').removeClass('z-40');
  $('#runButtonContainer').removeClass('z-40');

  $('#speak_container').addClass('z-40 bg-white relative');

  addHighlightBorder("speak_container");

  relocatePopup(50, 30);
  tutorialPopup(current_step);
}

function runSpeakAloudStep() {
  $('#editor').addClass('z-40');
  $('#code_output').addClass('z-40');
  $('#runButtonContainer').addClass('z-40');

  relocatePopup(50, 70);
  tutorialPopup(current_step);
}

function nextLevelStep() {
  removeBorder("speak_container");
  $('#editor').removeClass('z-40');
  $('#code_output').removeClass('z-40');
  $('#runButtonContainer').removeClass('z-40');
  $('#speak_container').removeClass('z-40 bg-white relative');

  $('#next_level_button').addClass("z-40");
  $('#next_level_button').removeAttr('onclick');
  addHighlightBorder("next_level_button");

  relocatePopup(50, 30);
  tutorialPopup(current_step);
}

function levelDefaultStep() {
  removeBorder("next_level_button");
  $('#next_level_button').removeClass('z-40');

  $('#code_content_container').addClass('z-40');
  $('#adventures').addClass('z-40 bg-gray-100');
  $('#adventures').show();

  // Set to false, prevent "are you sure you want to switch without saving" pop-up
  window.State.unsaved_changes = false;

  addHighlightBorder("adventures");
  relocatePopup(50, 40);
  tutorialPopup(current_step);
}

function adventureTabsStep() {
  $('#adventures-buttons').children().each(function() {
    if ($(this).attr('data-tab') == "story") {
      // Set to false, prevent "are you sure you want to switch without saving" pop-up
      window.State.unsaved_changes = false;
      $(this).click();
    }
  });

  tutorialPopup(current_step);
}

function quizTabStep() {
  tutorialPopup(current_step);
}

function saveShareStep() {
  removeBorder("adventures");
  $('#code_content_container').removeClass('z-40');
  $('#level-header').addClass("z-40");
  $('#cheatsheet_container').hide();
  addHighlightBorder("level-header");

  $('#save_program_button').removeAttr('onclick');
  $('#share_program_button').removeAttr('onclick');

  relocatePopup(50, 30);
  tutorialPopup(current_step);
}

function cheatsheetStep() {
  $('#cheatsheet_container').show();
  $('#code_output').removeClass('z-40');
  $('#adventures').removeClass('z-40');
  $('#cheatsheet_dropdown').addClass('z-40');
  $('#cheatsheet_dropdown').show();

  tutorialPopup(current_step);
}

function endTutorial() {
  removeBorder("level-header");
  $('#level-header').removeClass('z-40');
  $('#cheatsheet_dropdown').removeClass('z-40');
  $('#cheatsheet_dropdown').hide();

  relocatePopup(50, 15);
  tutorialPopup(current_step);
}

function callNextStep() {
  if (current_step == 2) {
    codeEditorStep();
  } else if (current_step == 3) {
    codeOutputStep();
  } else if (current_step == 4) {
    runButtonStep();
  } else if (current_step == 5) {
    tryRunButtonStep();
  } else if (current_step == 6) {
    speakAloudStep();
  } else if (current_step == 7) {
    runSpeakAloudStep();
  } else if (current_step == 8) {
    nextLevelStep();
  } else if (current_step == 9) {
    levelDefaultStep();
  } else if (current_step == 10) {
    adventureTabsStep();
  } else if (current_step == 11) {
    quizTabStep();
  } else if (current_step == 12) {
    saveShareStep();
  } else if (current_step == 13) {
    cheatsheetStep();
  } else if (current_step == 14) {
    pushAchievement("well_begun_is_half_done");
    $('#achievement_pop-up').removeClass('z-10');
    $('#achievement_pop-up').addClass('z-50');
    // If the achievement pop-up is visible -> wait with the next function call
    setTimeout(function(){
      if ($('#achievement_pop-up').is(':visible')) {
        setTimeout(function() {
          endTutorial();
          $('#achievement_pop-up').removeClass('z-50');
          $('#achievement_pop-up').addClass('z-10');
        }, 5000);
      } else {
        endTutorial();
        $('#achievement_pop-up').removeClass('z-50');
        $('#achievement_pop-up').addClass('z-10');
      }
    }, 500);
  } else {
    location.replace("/hedy");
  }
}

function classStep() {
  $('#auth_main_container').addClass('z-40');
  $('#teacher_classes').addClass('z-40 bg-gray-100');
  addHighlightBorder("teacher_classes");

  relocatePopup(50, 40);
  tutorialPopup(current_step);
}

function customizeClassStep() {
  tutorialPopup(current_step);
}

function adventureStep() {
  $('#teacher_adventures').addClass('z-40 bg-gray-100');
  removeBorder("teacher_classes");
  addHighlightBorder("teacher_adventures");

  relocatePopup(50, 70);
  tutorialPopup(current_step);
}

function multipleAccountsStep() {
  $('#teacher_accounts').addClass('z-40 bg-gray-100');
  removeBorder("teacher_adventures");
  addHighlightBorder("teacher_accounts");

  relocatePopup(50, 20);
  tutorialPopup(current_step);
}

function documentationStep() {
  $('#teacher_documentation').addClass('z-40 bg-gray-100');
  removeBorder("teacher_accounts");
  addHighlightBorder("teacher_documentation")

  tutorialPopup(current_step);
}

function teacherEndStep() {
  removeBorder("teacher_documentation");
  tutorialPopup(current_step);
}

function callTeacherNextStep() {
  if (current_step == 2) {
    classStep();
  } else if (current_step == 3) {
    customizeClassStep();
  } else if (current_step == 4) {
    adventureStep();
  } else if (current_step == 5) {
    multipleAccountsStep();
  } else if (current_step == 6) {
    documentationStep();
  } else if (current_step == 7) {
    pushAchievement("ring_the_bell");
    $('#achievement_pop-up').removeClass('z-10');
    $('#achievement_pop-up').addClass('z-50');
    // If the achievement pop-up is visible -> wait with the next function call
    setTimeout(function(){
      if ($('#achievement_pop-up').is(':visible')) {
        setTimeout(function() {
          teacherEndStep();
          $('#achievement_pop-up').removeClass('z-50');
          $('#achievement_pop-up').addClass('z-10');
        }, 5000);
      } else {
        teacherEndStep();
        $('#achievement_pop-up').removeClass('z-50');
        $('#achievement_pop-up').addClass('z-10');
      }
    }, 500);
  } else {
    location.replace("/for-teachers");
  }
}

function addHighlightBorder(element_id: string) {
  $('#' + element_id).addClass('border-2 rounded-lg border-red-500');
}

function removeBorder(element_id: string) {
  $('#' + element_id).removeClass('border-2 border-red-500');
}

function relocatePopup(x: number, y: number) {
  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (x && y) {
    let left = x.toString() + "%"
    let top = y.toString() + "%"
    $('#tutorial-pop-up').css({'top': top, 'left': left});
  }

}

function tutorialPopup(step: number) {
  let route = "/get_tutorial_step/intro/"
  if (!student) {
    route = "/get_tutorial_step/teacher0/"
  }
  $.ajax({
    type: 'GET',
    url: route + step.toString(),
    dataType: 'json'
  }).done(function(response: any) {
      $('#tutorial_title').text(response.title);
      $('#tutorial_text').text(response.text);
      $('#tutorial-pop-up').fadeIn(800);
  }).fail(function(response) {
    modal.alert(response.responseText, 3000, true);
  });
}

export function startTutorial() {
  $('#tutorial-mask').show();
  $('#adventures').hide();
  $('#variables_container').hide();
  theGlobalEditor?.setValue("");

  current_step = 1;
  student = true;
  tutorialPopup(current_step);
}

export function startTeacherTutorial() {
  $('#tutorial-mask').show();
  current_step = 1;
  student = false;
  tutorialPopup(current_step);
}

