import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        redirect: "/home",
    },
    {
        path: "/",
        component: {
            render(c) {
                return c("router-view");
            },
        },
        children: [
            {
                path: "/home",
                name: "home",
                component: () => import("../views/Home.vue"),
            },
        ],
    },
];

const router = new VueRouter({ routes });
export default router;