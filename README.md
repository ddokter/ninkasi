# Ninkasi - Brewery QC system

Ninkasi is meant to assist in quality control during the production of
beer. The focus of the system is registration of measurements during
this process. The main words that make up the vocabulary of Ninkasi is
a _batch_, that is one production of an amount of beer. A batch is
made up of one or more _brews_, to allow for combined brews into one
fermenter. The split, somewhat arbitrary but not unconventional, is
seen throughout the system. A brew is what happens on the _brewhouse_,
after transfer to a fermenter of other vessel all is related to a
batch.

Measurements are registerd in two different ways. The first is simply
the facility of noting down different kinds of measurements for any
given batch (or brew) of beer during the production. The other, less
obvious way, is that the system is designed such that it invites the
user to define a batch by measured processing steps. Although a batch
follows a recipe, the recipe steps are not copied to the batch. The
brewer needs to follow the recipe during brewing and register actual
steps of the process to a batch. This way, a more realistic picture
arises of the way the batch was really produced. The recipe is the
blueprint or plan, the batch with related brews is what actually
happened. This means that Ninkasi is meant to be used by *involved*
brewers, that are willing and able to find the time to regsiter what
they are doing.


## Design decisions

A batch consists of one or more brews, to be able to brew one single
batch over more brewhouse sessions. A brew can therefore also differ,
to compensate for a first brew of a batch. You may or may not like the
way the system works.


### Inline forms

Inline forms are used in two cases:

    1. the relation between two classes holds properties
	2. it is convenient to add more than one child per edit

In all other cases, sublistings or 'add' actions are provided on the
detail screen of the parent.


### Features

The main screen of Ninkasi is a dashboard, where the tasks that need
to be done appear. Most tasks are the result of business rules, of
brews. A business rule could be: after a brew, the brewhouse needs to
be CIP-ed within X days, or before transfer to a tank it needs to be
sanitized.

	* task list
	* batch nrs on stock
	* inventory. Batches affect the inventory numbers
	* if not enough stock, order task is created
	* 



### Batch

A batch is a volume of produce, from brewing untill packaging and
beyond. For the brewery, the batch is real presence untill it is sent
off, from there on it is something that can be tracked. So batch needs
to be 'somewhere' in the brewery. Untill packaging this is in a
container. Part of the batch is the brewing stage, when the volume is
in a brewhouse. After that, it is in some tank for fermentation,
maturation, packaging, etc.

The life cycle of a batch in terms of fermentation, maturation,
etc. does not need to be in line with the actual containers, although
usually it is. Therefore, actual location of the batch in the brewery
is a separate administration. Nothing prevents the end user from
splitting a batch over multiple containers.

When a batch is planned, the system keeps track of space
available. Whenever there is no space, no batch can be planned.
