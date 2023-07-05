# ninkasi
Brewery QA system


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
