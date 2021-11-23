import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';

const mutationSubject$ = new Subject<MutationRecord[]>();
const targetDOM = document.body;

const mutationObserver = new MutationObserver((mutations) => {
  mutationSubject$.next(mutations);
});
mutationObserver.observer(targetDOM, { attributes: true, subtree: true });

mutationSubject$
  .pipe(
    debounceTime(200),
  ).subscribe((mutations) => {
    // do somethings...
  });


