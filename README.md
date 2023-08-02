# Ninkasi - Brewery QC system

Ninkasi is meant to assist in quality control during the production of
beer. The focus of the system is measurement registration in two
ways. The first is simply the facility of noting down different kinds
of measurements for any given batch of beer during the production. The
other, less obvious way, is that the system is designed such that it
invites the user to define a batch by measured processing
steps. Although a batch follows a recipe, the recipe steps are not
copied to the batch. The brewer needs to follow the recipe during
brewing and register actual steps of the process to a batch. This way,
a more realistic picture arises of the way the batch was really
produced. The recipe is the blueprint or plan, the batch with related
brews is what actually happened.



## Design decisions

A batch consists of one or more brews, to be able to brew one single
batch over more brewhouse sessions. A brew can therefore also differ,
to compensate for a first brew of a batch.

### Inline forms

Inline forms are used in two cases:

    1. the relation between two classes holds properties
	2. it is convenient to add more than one child per edit

In all other cases, sublistings or 'add' actions are provided on the
detail screen of the parent.
