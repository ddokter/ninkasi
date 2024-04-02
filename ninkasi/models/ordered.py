from django.core.exceptions import ObjectDoesNotExist


class OrderedContainer:

    """ Maintain some order... """

    def get_child_qs(self):

        """ Implement this method to recieve the right QS """

        return {}

    def move(self, phase_id, amount):

        """ Move one up or one down """

        qs = self.get_child_qs()

        current = qs.get(pk=phase_id)

        try:
            target = qs.get(order=current.order + int(amount))

            tgt_order = target.order
            cur_order = current.order

            current.order = tgt_order
            target.order = cur_order

            current.save()
            target.save()

            return True

        except ObjectDoesNotExist:

            return False
