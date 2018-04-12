The files contain question schemes that we want to be answered for each area (filename)
The files are in the following format.

concept \t property \t reverse \t multipleTriples \t factual

======================================================================================================
concept:			type of the entity to be answered.
property:			property to be answered.
reverse:			if the triple's S, O has been changed, True. Otherwise, False.
multipleTriples: 	if the (S,P) can have more than one triple, True. Otherwise, False.
factual:			if the question type is factual, "factual". Otherwise, question type is opinion, "opinion".
======================================================================================================