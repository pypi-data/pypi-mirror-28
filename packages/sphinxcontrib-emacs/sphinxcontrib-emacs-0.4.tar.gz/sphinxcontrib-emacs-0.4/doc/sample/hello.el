(defcustom greeting "Hello %s!"
  "The greeting to use in `greet'.

The value of this variable should contain is used as string for
`format', with the only argument being the name of the user to
greet."
  :safe #'stringp
  :package-version '(hello . "0.1"))

(make-variable-buffer-local 'greeting)

(defun greet (name)
  "Greet the user with the given NAME, in classic Hello world style.

When called interactively, prompt for NAME.

Use the message template from `greeting' to assemble the greeting
mesage.

See URL `http://en.wikipedia.org/wiki/Hello_world_program'."
  (interactive "sYour name: ")
  (message greeting name))

(global-set-key (kbd "C-c g") #'greet)
