<?php
$conName = $_POST['con2Name'];
$conEmail = $_POST['con2Email'];
$conSubject = $_POST['con2Subject'];
$conMessage = $_POST['con2Message'];

ini_set('display_errors', 1);
error_reporting(E_ALL);

/**
 * Set the recipient email address.
 * 
 * FIXME: Update this to your desired email address.
 */
$recipient = "support@themejunction.net";

// Set the email subject.
$sender = $conSubject;


//Email Header
$head = "You have a new message from your Webency website Contact Form 2\n=============================";

// Build the email content.
$form_content = "$head\n\n";

$form_content .= "Full Name: $conName\n";

$form_content .= "Subject: $conSubject\n";

$form_content .= "Email: $conEmail\n";

$form_content .= "Message: \n$conMessage\n";


// Build the email headers.
$headers = "From: $conName < $conEmail >\r\n" .
  "Reply-To:" . $conEmail . "\r\n" .
  'X-Mailer: PHP/' . phpversion();

if (mail($recipient, $sender, $form_content, $headers)) {
  echo "Y";
} else {
  echo "N";
}
